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
            token = self.service.token(request.email, request.password)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if token:
                hash_key = EncryptUtils.encoded_hash(request.password, introspect_token['sub'])
                return auth_messages.AuthRes(
                    access_token=token['access_token'],
                    expires_in=token['expires_in'],
                    refresh_expires_in=token['refresh_expires_in'],
                    refresh_token=token['refresh_token'],
                    token_type=token['token_type'],
                    session_state=token['session_state'],
                    scope=token['scope'],
                    hash_key=EncryptUtils.encoded_hash(request.password, introspect_token['sub']),
                    base_response=auth_messages.BaseResponse(success=True)
                )
            else:
                raise Exception(Message.AUTH_USER_NOT_FOUND)

        except Exception as e:
            errors = [Message.get_error_object(e.args[0])]
            logger.error(errors)
            return auth_messages.AuthRes(
                base_response=auth_messages.BaseResponse(
                    success=False,
                    errors=auth_messages.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
            ))
       

    def register(self, request, context):
        # check exist user
        try:
            exists_user = self.service.get_user_id_by_email(request.email)
            if exists_user:
                raise Exception(Message.REGISTER_USER_ALREADY_EXISTS)

            # register new user
            new_user = self.service.register_user(request.email, request.password)

            if new_user:
                # create new user in database
                UserService().create_new_user(new_user, request, 'account')
                return auth_messages.RegisterRes(
                    base_response=auth_messages.BaseResponse(
                        success=True
                    ))
            else:
                self.service.delete_user(new_user)
                raise Exception(Message.REGISTER_USER_FAILED)
        except Exception as e:
            errors = [Message.get_error_object(e.args[0])]
            logger.error(errors)
            return auth_messages.RegisterRes(
                base_response=auth_messages.BaseResponse(
                    success=False,
                    errors=auth_messages.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
            ))


    def fogot_password(self, request, context):
        try:
            self.service.send_forgot_password(request.email)
            return auth_messages.BaseResponse(
                success=True
            )
        except Exception as e:
            errors = [Message.get_error_object(e.args[0])]
            logger.error(errors)
            return auth_messages.BaseResponse(
                    success=False,
                    errors=auth_messages.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
            )