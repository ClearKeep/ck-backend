from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.workspace import WorkspaceService
from protos import group_pb2, workspace_pb2
from utils.config import *
from src.controllers.group import GroupController
from src.models.group import GroupChat
from src.models.user import User
import json
from client.client_workspace import ClientWorkspace


class WorkspaceController(BaseController):
    def __init__(self, *kwargs):
        self.service = WorkspaceService()

    @request_logged
    async def workspace_info(self, request, context):
        try:
            owner_workspace_domain = get_owner_workspace_domain()
            if request.workspace_domain == owner_workspace_domain:
                return workspace_pb2.BaseResponse(success=True)
            else:
                workspace_info = ClientWorkspace().get_workspace_info(request.workspace_domain)
                if workspace_info:
                    return workspace_info
                else:
                    return workspace_pb2.BaseResponse(success=False)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_WORKSPACE_INFO_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def leave_workspace(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            user_info = User().get(client_id)
            lst_joined_group = GroupChat().get_joined(client_id)
            if len(lst_joined_group) > 0:

                for group in lst_joined_group:
                    request_leave_group = group_pb2.LeaveGroupRequest(
                        leave_member=group_pb2.MemberInfo(
                            id=client_id,
                            display_name=user_info.display_name,
                            workspace_domain=get_owner_workspace_domain()
                        ),
                        leave_member_by=group_pb2.MemberInfo(
                            id=client_id,
                            display_name=user_info.display_name,
                            workspace_domain=get_owner_workspace_domain()
                        ),
                        group_id=group.GroupChat.id
                    )
                    await GroupController().leave_group(request_leave_group, context)

            user_info.delete()
            KeyCloakUtils.delete_user(client_id)

            return workspace_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.LEAVE_WORKSPACE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

