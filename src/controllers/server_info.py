from src.controllers.base import *
from middlewares.request_logged import *
from src.services.server_info import ServerInfoService
from protos import server_info_pb2
import threading


class ServerInfoController(BaseController):
    def __init__(self, *kwargs):
        self.service = ServerInfoService()

    @request_logged
    async def update_nts(self, request, context):
        try:
            stun = request.stun
            turn = request.turn
            self.service.update_server_info(stun, turn)
            return server_info_pb2.BaseResponse(
                success=True
            )
        except Exception as e:
            logger.error(e)
            return server_info_pb2.BaseResponse(
                success=False
            )

    async def total_thread(self, request, context):
        try:
            return server_info_pb2.GetThreadResponse(
                total=threading.activeCount()
            )
        except Exception as e:
            logger.error(e)
