from __future__ import print_function

import grpc

from protos import user_pb2, user_pb2_grpc


class ClientUser:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def get_user_info(self, client_id, domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, domain=domain)
            response = self.stub.get_user_info(request)
            return response
        except:
            return None

    def get_user_signal_key(self, client_id, domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, domain=domain)
            response = self.stub.get_user_info(request)
            return response
        except:
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
