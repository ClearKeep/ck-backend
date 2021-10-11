from __future__ import print_function
import grpc
from protos import message_pb2_grpc
from utils.logger import *


class ClientMessage:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return message_pb2_grpc.MessageStub(channel)


    def get_messages_in_group(self, request):
        try:
            response = self.stub.workspace_get_messages_in_group(request)
            return response
        except Exception as e:
            logger.error(e)
            return None

    def publish_message(self, request):
        try:
            response = self.stub.Publish(request)
            return response
        except Exception as e:
            logger.error(e)
            return None

    def workspace_publish_message(self, request):
        try:
            response = self.stub.workspace_publish(request)
            return response
        except Exception as e:
            logger.error(e)
            return None
