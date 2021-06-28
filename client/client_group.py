from __future__ import print_function
import grpc
from protos import group_pb2, group_pb2_grpc
from utils.logger import *


class ClientGroup:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return group_pb2_grpc.GroupStub(channel)

    def create_group_workspace(self, request):
        try:
            response = self.stub.create_group_workspace(request)
            return response
        except Exception as e:
            logger.error(e)
            return None
