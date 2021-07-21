from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.workspace import WorkspaceService
from protos import group_pb2, workspace_pb2
from utils.config import *
from src.controllers.group import GroupController
from src.models.group import GroupChat


class WorkspaceController(BaseController):
    def __init__(self, *kwargs):
        self.service = WorkspaceService()

    @request_logged
    async def workspace_info(self, request, context):
        try:
            obj_res = self.service.get_joined_workspaces(request.client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def leave_workspace(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            lst_joined_group = GroupChat().get_joined(client_id)

            for group in lst_joined_group:
                request_leave_group = group_pb2.LeaveGroupRequest(
                    member_info=group_pb2.MemberInfo(
                        id=client_id,
                        display_name="",
                        workspace_domain=get_owner_workspace_domain(),
                        status=""
                    ),
                    group_id=group.id
                )
                GroupController().leave_group(request_leave_group, context)

            return workspace_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @request_logged
    # async def join_workspace(self, request, context):
    #     try:
    #         # header_data = dict(context.invocation_metadata())
    #         # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
    #         # client_id = introspect_token['sub']
    #         workspace_domain = request.workspace_domain
    #         client_id = request.client_id
    #         obj_res = self.service.join_workspace(client_id, workspace_domain)
    #         return obj_res
    #     except Exception as e:
    #         logger.error(e)
    #         errors = [Message.get_error_object(Message.JOIN_WORKSPACE_FAILED)]
    #         context.set_details(json.dumps(
    #             errors, default=lambda x: x.__dict__))
    #         context.set_code(grpc.StatusCode.INTERNAL)
    #
    # @request_logged
    # async def get_joined_workspaces(self, request, context):
    #     try:
    #         # header_data = dict(context.invocation_metadata())
    #         # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
    #         # client_id = introspect_token['sub']
    #         obj_res = self.service.get_joined_workspaces(request.client_id)
    #         return obj_res
    #     except Exception as e:
    #         logger.error(e)
    #         errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
    #         context.set_details(json.dumps(
    #             errors, default=lambda x: x.__dict__))
    #         context.set_code(grpc.StatusCode.INTERNAL)