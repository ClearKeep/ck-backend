from src.services.base import BaseService
from src.models.workspace import Workspace
from protos import workspace_pb2
import uuid


class WorkspaceService(BaseService):
    def __init__(self):
        super().__init__(Workspace())

    def join_workspace(self, client_id, workspace_domain, is_own_workspace):
        workspace_id = str(uuid.uuid4())
        self.model = Workspace(
            id=workspace_id,
            client_id=client_id,
            workspace_domain=workspace_domain,
            is_own_workspace=is_own_workspace
        )
        return workspace_pb2.BaseResponse(success=True)

    def get_joined_workspaces(self, client_id):
        lst_workspace = self.model.get_joined_workspaces(client_id)

        lst_obj_res = []
        for obj in lst_workspace:
            obj_res = workspace_pb2.WorkspaceObjectResponse(
                workspace_id=obj.id,
                workspace_domain=obj.workspace_domain,
                is_default_workspace=obj.is_default_workspace,
                is_own_workspace=obj.is_own_workspace
            )
            lst_obj_res.append(obj_res)

        response = workspace_pb2.GetJoinedWorkspaceResponse(
            lst_workspace=lst_obj_res
        )
        return response


