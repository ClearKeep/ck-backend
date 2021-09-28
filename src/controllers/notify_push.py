from protos import notify_push_pb2
from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.notify_push import NotifyPushService


class NotifyPushController(BaseController):
    def __init__(self, *kwargs):
        self.service = NotifyPushService()

    @request_logged
    @auth_required
    async def register_token(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            device_id = request.device_id
            token = request.token
            device_type = request.device_type

            self.service.register_token(client_id, device_id, device_type, token)
            return notify_push_pb2.BaseResponse()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_REGISTER_NOTIFY_TOKEN_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def push_text(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # client_id = introspect_token['sub']
            title = request.title
            body = request.body
            notify_type = request.notify_type
            custom_data = request.custom_data
            to_client_id = request.to_client_id
            self.service.push_text_to_client(to_client_id=to_client_id, title=title, body=body, notify_type=notify_type, data=custom_data)
            return notify_push_pb2.BaseResponse()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_REGISTER_NOTIFY_TOKEN_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def push_voip(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # client_id = introspect_token['sub']
            str_payload = request.payload
            payload = json.loads(str_payload)
            to_client_id = request.to_client_id

            await self.service.push_voip_client(to_client_id=to_client_id, payload=payload)
            return notify_push_pb2.BaseResponse()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_REGISTER_NOTIFY_TOKEN_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
