from __future__ import print_function
import grpc
from protos import notify_push_pb2, notify_push_pb2_grpc
from utils.const import GRPC_TIMEOUT
import logging
logger = logging.getLogger(__name__)


class ClientPush:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return notify_push_pb2_grpc.NotifyPushStub(channel)

    def push_text(self, request):
        try:
            response = self.stub.push_text(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def push_voip(self, to_client_id, payload):
        try:
            request = notify_push_pb2.PushVoipRequest(
                to_client_id=to_client_id,
                payload=payload
            )
            self.stub.push_voip(request, timeout=GRPC_TIMEOUT)
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def update_call(self, request):
        try:
            response = self.stub.update_call(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
