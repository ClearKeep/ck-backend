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
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # from_client_id = introspect_token['sub']
            from_client_id = '69e918f5-053d-4e7c-840f-7d80e9f4490f'
            group_id = request.group_id
            client_id = request.client_id
            self.service.request_call(group_id, from_client_id, client_id)

            return video_call_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
