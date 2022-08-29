import logging

from grpc.aio import insecure_channel
from protos import signal_pb2, signal_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

logger = logging.getLogger(__name__)


class ClientSignal:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return signal_pb2_grpc.SignalKeyDistributionStub(channel)

    @workspace_tolerance
    async def group_get_client_key(self, group_id, client_id):
        request = signal_pb2.GroupGetClientKeyRequest(groupId=group_id, clientId=client_id)
        return await self.stub.GroupGetClientKey(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_get_user_signal_key(self, client_id, workspace_domain):
        request = signal_pb2.PeerGetClientKeyRequest(clientId=client_id, workspace_domain=workspace_domain)
        return await self.stub.WorkspacePeerGetClientKey(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_group_get_client_key(self, group_id, client_id):
        request = signal_pb2.WorkspaceGroupGetClientKeyRequest(groupId=group_id, clientId=client_id)
        return await self.stub.WorkspaceGroupGetClientKey(request, timeout=GRPC_TIMEOUT)
