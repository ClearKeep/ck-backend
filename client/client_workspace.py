import logging

import grpc

from protos import workspace_pb2, workspace_pb2_grpc
from utils.const import GRPC_TIMEOUT

logger = logging.getLogger(__name__)


class ClientWorkspace:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return workspace_pb2_grpc.WorkspaceStub(channel)

    def get_workspace_info(self, workspace_domain):
        try:
            request = workspace_pb2.WorkspaceInfoRequest(workspace_domain=workspace_domain)
            response = self.stub.workspace_info(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
