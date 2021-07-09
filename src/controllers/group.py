from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.group import GroupService
from utils.config import get_owner_workspace_domain
from protos import group_pb2
from src.models.group import GroupChat
from client.client_group import *


class GroupController(BaseController):
    def __init__(self, *kwargs):
        self.service = GroupService()

    @request_logged
    async def create_group(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # created_by_client_id = introspect_token['sub']
            group_name = request.group_name
            group_type = request.group_type
            lst_client = request.lst_client
            obj_res = self.service.add_group(group_name, group_type, lst_client, request.created_by_client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def create_group_workspace(self, request, context):
        try:
            group_name = request.group_name
            group_type = request.group_type
            from_client_id = request.from_client_id
            client_id = request.client_id
            lst_client = request.lst_client
            owner_group_id = request.owner_group_id
            owner_workspace_domain = request.owner_workspace_domain
            obj_res = self.service.add_group_workspace(group_name, group_type, from_client_id, client_id, lst_client, owner_group_id,
                                                       owner_workspace_domain)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_group(self, request, context):
        try:
            group_id = request.group_id
            group = GroupChat().get_group(group_id)
            if not group.owner_workspace_domain:
                obj_res = self.service.get_group(group_id)
            else:
                get_group_request = group_pb2.GetGroupRequest(
                    group_id=group.owner_group_id
                )
                obj_res = ClientGroup(
                    group.owner_workspace_domain
                ).get_group(get_group_request)
                obj_res.group_id = group_id
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
    async def add_member(self, request, context):
        try:
            current_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(request.group_id)
            if (group.owner_workspace_domain and
                    group.owner_workspace_domain != current_workspace_domain):
                res_obj = self.service.add_member_to_group_not_owner(
                    request, group)
                return res_obj
            else:
                res_obj = self.service.add_member_to_group_owner(
                    request, group)
                return res_obj
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            return group_pb2.BaseResponse(
                success=False,
                errors=group_pb2.ErrorRes(
                    code=errors[0].code,
                    message=errors[0].message
                )
            )

    @request_logged
    async def add_member_workspace(self, request, context):
        try:
            obj_res = self.service.add_member_workspace(
                request.group_name,
                request.group_type,
                request.adding_member_id,
                request.adding_member_display_name,
                request.added_member_id,
                request.clients,
                request.owner_group_id,
                request.owner_workspace_domain,
                request.group_id,
                request.added_member_workspace_domain
            )
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def join_group(self, request, context):
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
