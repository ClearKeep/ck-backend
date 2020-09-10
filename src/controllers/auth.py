import grpc
import proto.auth_pb2_grpc as auth_service
import proto.auth_pb2 as auth_messages

from src.controllers.base import *
from src.services.auth import AuthService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils


class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()

    def Login(self, request, context):
        token = self.service.LoginUser(request.username, request.password)
        print("TYPE=", token['access_token'])
        print("expires_in=", token['expires_in'])
        if token:
            return auth_messages.AuthRes(
                access_token = token['access_token'],
                expires_in = token['expires_in'],
                refresh_expires_in = token['refresh_expires_in'],
                refresh_token = token['refresh_token'],
                token_type = token['token_type'],
                session_state = token['session_state'],
                scope = token['scope'])

        context.set_details('user is not found')
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return auth_messages.AuthRes()

    def Register(self, request, context):
        newUser = self.service.RegisterUser(
            request.email, request.username, request.password)
        if newUser:
            return auth_messages.RegisterRes(success=True)

        context.set_details('Can not create user')
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return auth_messages.AuthRes()
