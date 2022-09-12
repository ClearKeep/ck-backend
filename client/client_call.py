import logging
from grpc.aio import insecure_channel

from protos import video_call_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

logger = logging.getLogger(__name__)


class ClientVideoCall:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return video_call_pb2_grpc.VideoCallStub(channel)

    @workspace_tolerance
    async def workspace_video_call(self, request):
        return await self.stub.workspace_video_call(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_update_call(self, request):
        return await self.stub.workspace_update_call(request, timeout=GRPC_TIMEOUT)
