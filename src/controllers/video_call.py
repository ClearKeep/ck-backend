from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService


class VideoCallController(BaseController):
    def __init__(self, *kwargs):
        self.service = VideoCallService()

    @request_logged
    async def video_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id
            client_id = request.client_id
            obj_res = await self.service.request_call(group_id, from_client_id, client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def cancel_request_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id
            client_id = request.client_id
            obj_res = await self.service.cancel_request_call(group_id, from_client_id, client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_CANCEL_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
