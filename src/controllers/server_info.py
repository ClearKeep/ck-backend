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
            return server_info_pb2.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_SERVER_INFO_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def total_thread(self, request, context):
        try:
            return server_info_pb2.GetThreadResponse(
                total=threading.activeCount()
            )
        except Exception as e:
            logger.error(e)
