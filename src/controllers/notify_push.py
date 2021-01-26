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
    def register_token(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            device_id = request.device_id
            token = request.token
            device_type = request.device_type

            self.service.register_token(client_id, device_id, device_type, token)

            server_info = self.service.get_server_info()
            stun_server = notify_push_pb2.StunServer(
                server = server_info.turn_server.get("server"),
                port = server_info.turn_server.get("port")
            )
            turn_server = notify_push_pb2.TurnServer(
                server=server_info.turn_server.get("server"),
                port=server_info.turn_server.get("port"),
                type=server_info.turn_server.get("type"),
                user=server_info.turn_server.get("user"),
                pwd=server_info.turn_server.get("pwd")
            )
            return notify_push_pb2.ServerResponse(
                stun_server= server_info.stun_server,
                turn_server= server_info.turn_server
            )

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REGISTER_NOTIFY_TOKEN_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)