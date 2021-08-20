import protos.user_pb2 as user_messages
from src.controllers.base import *
from src.services.user import UserService
from middlewares.permission import *
from middlewares.request_logged import *
from utils.logger import *
from utils.config import *
from client.client_user import *


class UserController(BaseController, user_pb2_grpc.UserServicer):
    def __init__(self, *kwargs):
        self.service = UserService()

    # @auth_required
    async def change_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            self.service.change_password(request, request.old_password, request.new_password, introspect_token['sub'])
            return user_messages.BaseResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def get_mfa_state(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token or 'sub' not in introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            mfa_enable = self.service.get_mfa_state(client_id)
            return  user_messages.MfaStateResponse(
                mfa_enable=mfa_enable,
            )
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def enable_mfa(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token or 'sub' not in introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.init_mfa_state_enabling(client_id)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def disable_mfa(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.init_mfa_state_disabling(client_id)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def mfa_validate_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.validate_password(client_id, request.password)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def mfa_validate_otp(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.validate_otp(client_id, request.otp)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def mfa_resend_otp(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.re_init_otp(client_id)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    # @request_logged
    async def get_profile(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            user_info = self.service.get_profile(client_id, header_data['hash_key'])
            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_PROFILE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def update_profile(self, request, context):
        logger.info("user update_profile api")
        try:
            display_name = request.display_name
            avatar = request.avatar
            phone_number = request.phone_number

            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            self.service.update_profile(client_id, display_name, phone_number, avatar)
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_PROFILE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    # @request_logged
    async def get_user_info(self, request, context):
        try:
            client_id = request.client_id
            client_workspace_domain = request.workspace_domain
            owner_workspace_domain = get_owner_workspace_domain()

            if client_workspace_domain == owner_workspace_domain:
                user_info = self.service.get_user_info(client_id, owner_workspace_domain)
            else:
                client = ClientUser(client_workspace_domain)
                user_info = client.get_user_info(client_id=client_id, workspace_domain=client_workspace_domain)

            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_USER_INFO_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def search_user(self, request, context):
        logger.info("user search_user api")
        try:
            keyword = request.keyword
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            obj_res = self.service.search_user(keyword, client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_users(self, request, context):
        logger.info("user get_users api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            owner_workspace_domain = get_owner_workspace_domain()

            obj_res = self.service.get_users(client_id, owner_workspace_domain)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_user_domain(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            domain = "server.domain2"
            obj_res = self.service.get_users_domain(domain=domain)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # update status for user ("Active, Busy, Away, Do not disturb")
    @request_logged
    async def update_status(self, request, context):
        logger.info("user update_status api")
        try:
            status = request.status
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            self.service.set_user_status(client_id, status)
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_USER_STATUS_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def ping_request(self, request, context):
        logger.info("ping_request api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            self.service.update_client_record(client_id)
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.PING_PONG_SERVER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_clients_status(self, request, context):
        logger.info("get_client_status api")
        try:
            list_clients = request.lst_client
            should_get_profile = request.should_get_profile
            list_user_status = self.service.get_list_clients_status(list_clients,should_get_profile)
            return list_user_status
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_USER_STATUS_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def upload_avatar(self, request, context):
        logger.info("upload_avatar api")
        try:
            file_name = request.file_name
            file_content = request.file_data
            file_content_type = request.file_content_type
            file_hash = request.file_hash
            # client_id from headers
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            obj_res = self.service.upload_avatar(client_id, file_name, file_content, file_content_type, file_hash)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_USER_STATUS_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
