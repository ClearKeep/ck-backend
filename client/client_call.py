import logging

import grpc
from protos import video_call_pb2_grpc

logger = logging.getLogger(__name__)


class ClientVideoCall:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return video_call_pb2_grpc.VideoCallStub(channel)

    def video_call(self, request):
        try:
            response = self.stub.video_call(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_video_call(self, request):
        try:
            response = self.stub.workspace_video_call(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def cancel_request_call(self, request):
        try:
            response = self.stub.cancel_request_call(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_update_call(self, request):
        try:
            response = self.stub.workspace_update_call(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
