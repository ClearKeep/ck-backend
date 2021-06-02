from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService
from src.services.group import GroupService
from client.client_call import *


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
            call_type = request.call_type
            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])
            group = GroupService().get_group(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                request.group_id = group.owner_group_id
                obj_res = ClientVideoCall(group.owner_workspace_domain).video_call(request)
                if obj_res:
                    return obj_res
                else:
                    raise
            else:
                obj_res = await self.service.request_call(call_type, group_id, from_client_id, client_id)
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
            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])
            group = GroupService().get_group(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                request.group_id = group.owner_group_id
                obj_res = ClientVideoCall(group.owner_workspace_domain).cancel_request_call(request)
                if obj_res:
                    return obj_res
                else:
                    raise
            else:
                obj_res = await self.service.cancel_request_call(group_id, from_client_id, client_id)
                return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_CANCEL_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def update_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id
            # client_id = request.client_id
            update_type = request.update_type

            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])
            group = GroupService().get_group(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                request.group_id = group.owner_group_id
                obj_res = ClientVideoCall(group.owner_workspace_domain).update_call(request)
                if obj_res:
                    return obj_res
                else:
                    raise
            else:
                obj_res = self.service.update_call(update_type, group_id, from_client_id)
                return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_UPDATE_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
