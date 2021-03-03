import protos.auth_pb2 as auth_messages
from src.controllers.base import BaseController
from src.services.auth import AuthService
from src.services.user import UserService
from utils.encrypt import EncryptUtils
from middlewares.permission import *
from middlewares.request_logged import *


class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()
        self.user_service = UserService()

    @request_logged
    async def login(self, request, context):
        print("auth login api")
        try:
            token = self.service.token(request.email, request.password)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if token:
                self.user_service.update_last_login(user_id=introspect_token['sub'])
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
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
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
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
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
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            return auth_messages.BaseResponse(
                success=False,
                errors=auth_messages.ErrorRes(
                    code=errors[0].code,
                    message=errors[0].message
                )
            )

    @auth_required
    def logout(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            device_id = request.device_id
            refresh_token = request.refresh_token
            self.service.logout(refresh_token)
            self.service.remove_token(client_id=client_id, device_id=device_id)
            return auth_messages.BaseResponse(
                success=True
            )
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            return auth_messages.BaseResponse(
                success=False,
                errors=auth_messages.ErrorRes(
                    code=errors[0].code,
                    message=errors[0].message
                )
            )
