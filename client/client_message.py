import logging

from grpc.aio import insecure_channel
from protos import message_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance


logger = logging.getLogger(__name__)


class ClientMessage:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return message_pb2_grpc.MessageStub(channel)

    @workspace_tolerance
    async def workspace_get_messages_in_group(self, request):
        return await self.stub.workspace_get_messages_in_group(request, timeout=GRPC_TIMEOUT)
            
    @workspace_tolerance
    async def workspace_publish_message(self, request):
        return await self.stub.workspace_publish(request, timeout=GRPC_TIMEOUT)
