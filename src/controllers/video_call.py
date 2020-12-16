from protos import video_call_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService
from src.models.signal_group_key import GroupClientKey


class VideoCallController(BaseController):
    def __init__(self, *kwargs):
        self.service = VideoCallService()

    @request_logged
    def video_call(self, request, context):
        try:
            group_id = request.group_id
            from_client_id = request.from_client_id
            client_id = request.client_id

            from_client_username = ""
            list_client_push_token = []

            # send push notification to all member of group
            lst_client_in_groups = GroupClientKey().get_clients_in_groups(group_id)
            for client in lst_client_in_groups:
                if client.client_id == from_client_id:
                    from_client_username = client.username
                else:
                    list_client_push_token.append(client.push_token)

            return video_call_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
