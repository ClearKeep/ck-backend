import grpc
import json
import protos.auth_pb2 as auth_messages
from src.controllers.base import BaseController
from src.services.auth import AuthService
from utils.keycloak import KeyCloakUtils
from msg.message import Message
from src.services.user import UserService
from utils.encrypt import EncryptUtils
from utils.logger import *

class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()
        self.user_service = UserService()

    def login(self, request, context):
        try:
            token = self.service.token(request.username, request.password)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if token:
                return auth_messages.AuthRes(
                    access_token=token['access_token'],
                    expires_in=token['expires_in'],
                    refresh_expires_in=token['refresh_expires_in'],
                    refresh_token=token['refresh_token'],
                    token_type=token['token_type'],
                    session_state=token['session_state'],
                    scope=token['scope'],
                    hash_key=EncryptUtils.encoded_hash(request.password, introspect_token['sub']),
                )
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            # return auth_messages.AuthRes()
       

    def register(self, request, context):
        # check exist user
        exists_user = self.service.get_user_id_by_username(request.username)
        if exists_user:
            errors = [Message.get_error_object(
                Message.REGISTER_USER_ALREADY_EXISTS)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return auth_messages.AuthRes()

        # register new user
        new_user = self.service.register_user(
            request.email, request.username, request.password)

        if new_user:
            # create new user in database
            UserService().create_new_user(new_user, request, 'account')
            return auth_messages.RegisterRes(success=True)

        # return error
        errors = [Message.get_error_object(Message.REGISTER_USER_FAILED)]
        context.set_details(json.dumps(
            errors, default=lambda x: x.__dict__))
        context.set_code(grpc.StatusCode.INTERNAL)
        # return auth_messages.AuthRes()
