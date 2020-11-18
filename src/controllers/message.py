from proto import group_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.message import MessageService


class MessageController(BaseController):
    def __init__(self, *kwargs):
        self.service = MessageService()

    @request_logged
    def get_messages_in_group(self, request, context):
        try:
            group_name = request.group_name
            group_type = request.group_type
            lst_client_id = request.lst_client_id
            obj_res = self.service.add_group(group_name, group_type, lst_client_id, request.created_by_client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
