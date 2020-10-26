import proto.user_pb2 as user_messages
from src.controllers.base import *
from src.services.user import UserService
from middlewares.permission import *
from utils.logger import *

class UserController(BaseController):
    def __init__(self, *kwargs):
        self.service = UserService()
    
    @auth_required
    def change_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            self.service.change_password(request, request.old_password, request.new_password, introspect_token['sub'])
            return user_messages.SuccessResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            # return user_messages.SuccessResponse()

    @auth_required
    def get_user_info(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_info = self.service.get_user_info(introspect_token['sub'], header_data['hash_key'])
            if user_info:
                return user_messages.UserInfoResponse(
                    id=user_info.id,
                    username=user_info.username,
                    email=user_info.email,
                    first_name=user_info.first_name,
                    last_name=user_info.last_name
                )

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            # return user_messages.UserInfoResponse()

    @auth_required
    def update_user_info(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            self.service.update_user_info(request, introspect_token['sub'], header_data['hash_key'])
            return user_messages.SuccessResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_USER_INFO_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            # return user_messages.UserInfoResponse()
