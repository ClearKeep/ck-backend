import logging
import asyncio
import grpc

from protos import group_pb2_grpc
from utils.const import GRPC_TIMEOUT

logger = logging.getLogger(__name__)


class ClientGroup:
    def __init__(self, workspace_domain):
        self.workspace_domain = workspace_domain
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return group_pb2_grpc.GroupStub(channel)

    def create_group_workspace(self, request):
        try:
            response = self.stub.create_group_workspace(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def add_member(self, request):
        try:
            response = self.stub.add_member(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_add_member(self, request):
        try:
            response = self.stub.workspace_add_member(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def get_group(self, request):
        try:
            response = self.stub.get_group(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def leave_group(self, request):
        try:
            response = self.stub.leave_group(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_leave_group(self, request):
        try:
            response = self.stub.workspace_leave_group(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    def workspace_notify_deactive_member(self, request):
        try:
            response = self.stub.workspace_notify_deactive_member(request, timeout=GRPC_TIMEOUT)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    async def workspace_member_forgot_password_in_group(self, request):
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(None, lambda: self.stub.workspace_member_forgot_password_in_group(request))
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_member_forgot_password_in_group in workspace {self.workspace_domain}')
            else:
                raise
    
    async def workspace_member_reset_pincode_in_group(self, request):
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(None, lambda: self.stub.workspace_member_reset_pincode_in_group(request))
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                logger.info(f'no workspace_member_forgot_password_in_group in workspace {self.workspace_domain}')
            else:
                raise
