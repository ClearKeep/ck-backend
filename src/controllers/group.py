from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.group import GroupService


class GroupController(BaseController):
    def __init__(self, *kwargs):
        self.service = GroupService()

    @request_logged
    async def create_group(self, request, context):
        print("group create_group api")
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # created_by_client_id = introspect_token['sub']
            group_name = request.group_name
            group_type = request.group_type
            lst_client_id = request.lst_client_id
            obj_res = self.service.add_group(group_name, group_type, lst_client_id, request.created_by_client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_group(self, request, context):
        print("group get_group api")
        try:
            group_id = request.group_id
            obj_res = self.service.get_group(group_id)
            if obj_res is not None:
                return obj_res
            else:
                errors = [Message.get_error_object(Message.GROUP_CHAT_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def search_groups(self, request, context):
        print("group search_groups api")
        try:
            keyword = request.keyword
            obj_res = self.service.search_group(keyword)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_joined_groups(self, request, context):
        print("group get_joined_groups api")
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # client_id = introspect_token['sub']
            obj_res = self.service.get_joined_group(request.client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def invite_to_group(self, request, context):
        print("group invite_to_group api")
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def join_group(self, request, context):
        print("group join_group api")
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
