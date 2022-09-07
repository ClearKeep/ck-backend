import logging
import asyncio
import grpc

from grpc.aio import insecure_channel
from protos import user_pb2, user_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

logger = logging.getLogger(__name__)


class ClientUser:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)
        self.workspace_domain = workspace_domain

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return user_pb2_grpc.UserStub(channel)

    @workspace_tolerance
    async def get_user_info(self, client_id, workspace_domain):
        request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
        return await self.stub.get_user_info(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def get_user_signal_key(self, client_id, workspace_domain):
        request = user_pb2.GetUserRequest(client_id=client_id, workspace_domain=workspace_domain)
        return await self.stub.get_user_info(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def get_clients_status(self, lst_client, should_get_profile):
        request = user_pb2.GetClientsStatusRequest(lst_client=lst_client, should_get_profile=should_get_profile)
        return await self.stub.get_clients_status(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def update_display_name(self, user_id, display_name):
        request = user_pb2.WorkspaceUpdateDisplayNameRequest(user_id=user_id, display_name=display_name)
        try:
            await self.stub.workspace_update_display_name(request, timeout=GRPC_TIMEOUT)
        except grpc.aio._call.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_update_display_name in workspace {self.workspace_domain}')
            else:
                raise

    @workspace_tolerance
    async def find_user_by_email(self, email):
        request = user_pb2.FindUserByEmailRequest(email=email)
        try:
            return await self.stub.workspace_find_user_by_email(request, timeout=GRPC_TIMEOUT)
        except grpc.aio._call.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_find_user_by_email in workspace {self.workspace_domain}')
                return
            else:
                raise
