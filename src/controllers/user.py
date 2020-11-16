import proto.user_pb2 as user_messages
from src.controllers.base import *
from src.services.user import UserService
from middlewares.permission import *
from middlewares.request_logged import *
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
            return user_messages.BaseResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)


    @auth_required
    @request_logged
    def get_profile(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_info = self.service.get_profile(introspect_token['sub'], header_data['hash_key'])
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

    @auth_required
    def update_profile(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            self.service.update_profile(request, introspect_token['sub'], header_data['hash_key'])
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_PROFILE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def get_user_info(self, request, context):
        try:
            client_id = request.client_id
            user_info = self.service.get_user_info(client_id)
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
    def search_user(self, request, context):
        try:
            keyword = request.keyword
            obj_res = self.service.search_user(keyword)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def get_users(self, request, context):
        try:
            obj_res = self.service.get_users("1")
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
