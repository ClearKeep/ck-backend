import logging
import asyncio
from grpc.aio import insecure_channel

from protos import group_pb2_grpc
from utils.const import GRPC_TIMEOUT
from client.utils import workspace_tolerance

logger = logging.getLogger(__name__)


class ClientGroup:
    def __init__(self, workspace_domain):
        self.workspace_domain = workspace_domain
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = insecure_channel(workspace_domain)
        return group_pb2_grpc.GroupStub(channel)

    @workspace_tolerance
    async def create_group_workspace(self, request):
        return await self.stub.create_group_workspace(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def add_member(self, request):
        return await self.stub.add_member(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_add_member(self, request):
        return await self.stub.workspace_add_member(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def leave_group(self, request):
        return await self.stub.leave_group(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_leave_group(self, request):
        return await self.stub.workspace_leave_group(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_notify_deactive_member(self, request):
        return await self.stub.workspace_notify_deactive_member(request, timeout=GRPC_TIMEOUT)

    @workspace_tolerance
    async def workspace_member_forgot_password_in_group(self, request):
        try:
            return await self.stub.workspace_member_forgot_password_in_group(request, timeout=GRPC_TIMEOUT)
        except grpc.aio._call.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_member_forgot_password_in_group in workspace {self.workspace_domain}')
            else:
                raise
    
    @workspace_tolerance
    async def workspace_member_reset_pincode_in_group(self, request):
        try:
            return await self.stub.workspace_member_reset_pincode_in_group(request, timeout=GRPC_TIMEOUT)
        except grpc.aio._call.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_member_forgot_password_in_group in workspace {self.workspace_domain}')
            else:
                raise
