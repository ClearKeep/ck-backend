from __future__ import print_function
import grpc
from protos import user_pb2, user_pb2_grpc
from utils.logger import *


class ClientUser:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return user_pb2_grpc.UserStub(channel)

    def get_user_info(self, client_id, workspace_domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
            response = self.stub.get_user_info(request)
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
        
    def get_client_status(self, lst_client):
        print("get_client_status",lst_client)
        try:
            request = user_pb2.GetClientsStatusRequest(lst_client=lst_client)
            response = self.stub.get_client_status(request)
            return response
        except:
            return None

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return user_pb2_grpc.UserStub(channel)
