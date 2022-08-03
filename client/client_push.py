from __future__ import print_function
from grpc.aio import insecure_channel
from protos import notify_push_pb2, notify_push_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

import logging
logger = logging.getLogger(__name__)


class ClientPush:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return notify_push_pb2_grpc.NotifyPushStub(channel)

    @workspace_tolerance
    async def push_text(self, request):
        return await self.stub.push_text(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def push_voip(self, to_client_id, payload):
        request = notify_push_pb2.PushVoipRequest(
            to_client_id=to_client_id,
            payload=payload
        )
        return await self.stub.push_voip(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def update_call(self, request):
        return await self.stub.update_call(request, timeout=GRPC_TIMEOUT)
