import logging

import grpc
from protos import user_pb2, user_pb2_grpc

logger = logging.getLogger(__name__)


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
            logger.error(e, exc_info=True)
            return None

    def get_user_signal_key(self, client_id, workspace_domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
            response = self.stub.get_user_info(request)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def get_clients_status(self, lst_client, should_get_profile):
        print("get_client_status",lst_client)
        try:
            request = user_pb2.GetClientsStatusRequest(lst_client=lst_client, should_get_profile=should_get_profile)
            response = self.stub.get_clients_status(request)
            return response
        except:
            return None
