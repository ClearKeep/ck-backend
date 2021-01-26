from protos import video_call_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService

class VideoCallController(BaseController):
    def __init__(self, *kwargs):
        self.service = VideoCallService()

    @request_logged
    def video_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']

            group_id = request.group_id
            client_id = request.client_id
            self.service.request_call(group_id, from_client_id, client_id)

            server_info = self.service.get_server_info()
            stun_server = video_call_pb2.Stun_Server(
                server = server_info.turn_server.get("server"),
                port = server_info.turn_server.get("port")
            )

            turn_server = video_call_pb2.Turn_Server(
                server=server_info.turn_server.get("server"),
                port=server_info.turn_server.get("port"),
                type=server_info.turn_server.get("type"),
                user=server_info.turn_server.get("user"),
                pwd=server_info.turn_server.get("pwd")
            )

            return video_call_pb2.ServerResponse(
                stun_server = stun_server,
                turn_server = turn_server
            )
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
