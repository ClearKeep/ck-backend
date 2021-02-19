from protos import notify_push_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.notify_push import NotifyPushService


class NotifyPushController(BaseController):
    def __init__(self, *kwargs):
        self.service = NotifyPushService()

    @request_logged
    async def register_token(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            device_id = request.device_id
            token = request.token
            device_type = request.device_type

            self.service.register_token(client_id, device_id, device_type, token)
            return notify_push_pb2.BaseResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REGISTER_NOTIFY_TOKEN_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)