from __future__ import print_function
import grpc
from protos import workspace_pb2, workspace_pb2_grpc
from utils.logger import *


class ClientWorkspace:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return workspace_pb2_grpc.WorkspaceStub(channel)

    def get_workspace_info(self, workspace_domain):
        try:
            request = workspace_pb2.WorkspaceInfoRequest(workspace_domain=workspace_domain)
            response = self.stub.workspace_info(request)
            return response
        except Exception as e:
            logger.error(e)
            return None

    def get_user_signal_key(self, client_id, workspace_domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
            response = self.stub.get_user_info(request)
            return response
        except Exception as e:
            logger.error(e)
            return None

    def get_clients_status(self, lst_client):
        print("get_client_status", lst_client)
        try:
            request = user_pb2.GetClientsStatusRequest(lst_client=lst_client)
            response = self.stub.get_clients_status(request)
            return response
        except:
            return None

