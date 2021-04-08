import protos.auth_pb2 as auth_messages
from src.controllers.base import BaseController
from src.services.auth import AuthService
from src.services.user import UserService
from src.services.message import MessageService
from src.services.notify_inapp import NotifyInAppService
from utils.encrypt import EncryptUtils
from middlewares.permission import *
from middlewares.request_logged import *


class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()
        self.user_service = UserService()

    @request_logged
    async def login(self, request, context):
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

    @request_logged
    async def login_google(self, request, context):
        try:
            token = self.service.google_login(request.id_token)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if token:
                #self.user_service.update_last_login(user_id=introspect_token['sub'])
                auth_response = auth_messages.AuthRes(
                    access_token=token['access_token'],
                    expires_in=token['expires_in'],
                    hash_key=EncryptUtils.encoded_hash(introspect_token['sub'], introspect_token['sub']),
                    base_response=auth_messages.BaseResponse(success=True)
                )
                if token['refresh_token']:
                    auth_response.refresh_token = token['refresh_token']
                if token['refresh_expires_in']:
                    auth_response.refresh_expires_in = token['refresh_expires_in']
                if token['token_type']:
                    auth_response.token_type = token['token_type']
                if token['session_state']:
                    auth_response.session_state = token['session_state']
                if token['scope']:
                    auth_response.scope = token['scope']

                return auth_response
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

    @request_logged
    async def login_office(self, request, context):
        try:
            token = self.service.office_login(request.access_token)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if token:
                #self.user_service.update_last_login(user_id=introspect_token['sub'])
                auth_response = auth_messages.AuthRes(
                    access_token=token['access_token'],
                    expires_in=token['expires_in'],
                    hash_key=EncryptUtils.encoded_hash(introspect_token['sub'], introspect_token['sub']),
                    base_response=auth_messages.BaseResponse(success=True)
                )
                if token['refresh_token']:
                    auth_response.refresh_token = token['refresh_token']
                if token['refresh_expires_in']:
                    auth_response.refresh_expires_in = token['refresh_expires_in']
                if token['token_type']:
                    auth_response.token_type = token['token_type']
                if token['session_state']:
                    auth_response.session_state = token['session_state']
                if token['scope']:
                    auth_response.scope = token['scope']

                return auth_response
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

    @request_logged
    async def register(self, request, context):
        # check exist user
        try:
            exists_user = self.service.get_user_id_by_email(request.email)
            if exists_user:
                raise Exception(Message.REGISTER_USER_ALREADY_EXISTS)

            # register new user
            new_user = self.service.register_user(request.email, request.password, request.display_name)

            if new_user:
                # create new user in database
                UserService().create_new_user(new_user, request.email, request.display_name,  'account')
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

    @request_logged
    async def fogot_password(self, request, context):
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
    @request_logged
    async def logout(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            device_id = request.device_id
            refresh_token = request.refresh_token
            self.service.logout(refresh_token)
            self.service.remove_token(client_id=client_id, device_id=device_id)
            MessageService().un_subscribe(client_id)
            NotifyInAppService().un_subscribe(client_id)

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
