import logging

import grpc
from protos import message_pb2_grpc

logger = logging.getLogger(__name__)


class ClientMessage:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return message_pb2_grpc.MessageStub(channel)


    def workspace_get_messages_in_group(self, request):
        try:
            response = self.stub.workspace_get_messages_in_group(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
            

    def workspace_publish_message(self, request):
        try:
            response = self.stub.workspace_publish(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
