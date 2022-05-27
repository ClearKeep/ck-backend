import logging

import grpc
from protos import signal_pb2, signal_pb2_grpc
from utils.const import GRPC_TIMEOUT

logger = logging.getLogger(__name__)


class ClientSignal:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return signal_pb2_grpc.SignalKeyDistributionStub(channel)

    def group_get_client_key(self, group_id, client_id):
        try:
            request = signal_pb2.GroupGetClientKeyRequest(groupId=group_id, clientId=client_id)
            response = self.stub.GroupGetClientKey(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_get_user_signal_key(self, client_id, workspace_domain):
        try:
            request = signal_pb2.PeerGetClientKeyRequest(clientId=client_id, workspace_domain=workspace_domain)
            response = self.stub.WorkspacePeerGetClientKey(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_group_get_client_key(self, group_id, client_id):
        try:
            request = signal_pb2.WorkspaceGroupGetClientKeyRequest(groupId=group_id, clientId=client_id)
            response = self.stub.WorkspaceGroupGetClientKey(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
