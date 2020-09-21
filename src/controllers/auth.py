import grpc
import json
import proto.auth_pb2_grpc as auth_service
import proto.auth_pb2 as auth_messages

from src.controllers.base import ErrorResponse, BaseController
from src.services.auth import AuthService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils
from msg.message import Message
from src.services.user import UserService
from utils.encrypt import EncryptUtils

class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()
        self.user_service = UserService()

    def login(self, request, context):
        try:
            token = self.service.token(request.username, request.password)

            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            user_info = self.user_service.find_by_id(introspect_token['sub'])

            if token:
                return auth_messages.AuthRes(
                    access_token=token['access_token'],
                    expires_in=token['expires_in'],
                    refresh_expires_in=token['refresh_expires_in'],
                    refresh_token=token['refresh_token'],
                    token_type=token['token_type'],
                    session_state=token['session_state'],
                    scope=token['scope'],
                    email=EncryptUtils.decrypt_data(user_info.email, request.password),
                    username=EncryptUtils.decrypt_data(user_info.username, request.password)
                    )
        except:
            # return error
            errors = []
            errors.append(Message.get_error_object(Message.AUTH_USER_NOT_FOUND))
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.NOT_FOUND)

            return auth_messages.AuthRes()
       

    def register(self, request, context):
        # check exist user
        existsUser = self.service.get_user_id_by_username(request.username)
        if existsUser:
            errors = []
            errors.append(Message.get_error_object(
                Message.REGISTER_USER_ALREADY_EXISTS))
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return auth_messages.AuthRes()

        # register new user
        newUser = self.service.register_user(
            request.email, request.username, request.password)

        if newUser:
            # create new user in database
            email = EncryptUtils.encrypt_data(request.email, request.password)
            username = EncryptUtils.encrypt_data(request.username, request.password)
            UserService().create_new_user(newUser, email, username, 'account')
            return auth_messages.RegisterRes(success=True)

        # return error
        errors = []
        errors.append(Message.get_error_object(Message.REGISTER_USER_FAILED))
        context.set_details(json.dumps(
            errors, default=lambda x: x.__dict__))
        context.set_code(grpc.StatusCode.INTERNAL)
        return auth_messages.AuthRes()
