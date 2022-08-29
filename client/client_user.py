import logging
import asyncio
import grpc
from protos import user_pb2, user_pb2_grpc
from utils.const import GRPC_TIMEOUT

logger = logging.getLogger(__name__)


class ClientUser:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)
        self.workspace_domain = workspace_domain

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return user_pb2_grpc.UserStub(channel)

    def get_user_info(self, client_id, workspace_domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
            response = self.stub.get_user_info(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def get_user_signal_key(self, client_id, workspace_domain):
        try:
            request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
            response = self.stub.get_user_info(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def get_clients_status(self, lst_client, should_get_profile):
        try:
            request = user_pb2.GetClientsStatusRequest(lst_client=lst_client, should_get_profile=should_get_profile)
            response = self.stub.get_clients_status(request, timeout=GRPC_TIMEOUT)
            return response
        except:
            return None

    async def update_display_name(self, user_id, display_name):
        loop = asyncio.get_running_loop()
        try:
            request = user_pb2.WorkspaceUpdateDisplayNameRequest(user_id=user_id, display_name=display_name)
            await loop.run_in_executor(None, lambda: self.stub.workspace_update_display_name(request, timeout=GRPC_TIMEOUT))
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_update_display_name in workspace {self.workspace_domain}')
            else:
                raise
