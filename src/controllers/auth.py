import grpc
import proto.auth_pb2_grpc as auth_service
import proto.auth_pb2 as auth_messages

from src.controllers.base import *
from src.services.auth import AuthService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils
from msg.message import Message
from src.services.user import UserService


class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()

    def login(self, request, context):
        token = self.service.login_user(request.username, request.password)
        print("TYPE=", token['access_token'])
        print("expires_in=", token['expires_in'])
        if token:
            return auth_messages.AuthRes(
                access_token=token['access_token'],
                expires_in=token['expires_in'],
                refresh_expires_in=token['refresh_expires_in'],
                refresh_token=token['refresh_token'],
                token_type=token['token_type'],
                session_state=token['session_state'],
                scope=token['scope'])

        context.set_details(Message().AUTH_USER_NOT_FOUND)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return auth_messages.AuthRes()

    def register(self, request, context):
        #print("Call register")
        # check exist user
        # existsUser = self.service.get_user_by_name(request.username)
        # print("existsUser=", existsUser)
        # if existsUser:
        #     context.set_details(Message().REGISTER_USER_ALREADY_EXISTS)
        #     context.set_code(grpc.StatusCode.ALREADY_EXISTS)
        #     return auth_messages.AuthRes()

        # register new user
        newUser = self.service.register_user(
            request.email, request.username, request.password)
        #print("newUser=", newUser)
        if newUser:
            # create new user in database
            UserService().create_new_user(newUser, request.email, request.username)
            return auth_messages.RegisterRes(success=True)

        context.set_details(Message().REGISTER_USER_FAILED)
        context.set_code(grpc.StatusCode.INTERNAL)
        return auth_messages.AuthRes()
