import logging

from grpc.aio import insecure_channel

from protos import workspace_pb2, workspace_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

logger = logging.getLogger(__name__)


class ClientWorkspace:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return workspace_pb2_grpc.WorkspaceStub(channel)

    @workspace_tolerance
    async def get_workspace_info(self, workspace_domain):
        request = workspace_pb2.WorkspaceInfoRequest(workspace_domain=workspace_domain)
        return await self.stub.workspace_info(request, timeout=GRPC_TIMEOUT)
