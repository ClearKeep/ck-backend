from client.client_push import ClientPush
from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService
from src.services.group import GroupService
from src.services.server_info import ServerInfoService
from src.services.notify_push import NotifyPushService
from client.client_call import *
import secrets


class VideoCallController(BaseController):
    def __init__(self, *kwargs):
        self.service = VideoCallService()
        self.service_group = GroupService()

    @request_logged
    async def video_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id

            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])

            group = GroupService().get_group_info(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                return await self.call_to_group_not_owner(request, group, from_client_id)
            else:
                return await self.call_to_group_owner(request, group, from_client_id)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_video_call(self, request, context):
        try:
            from_client_id = request.from_client_id
            from_client_name = request.from_client_name
            group_id = request.group_id
            client_id = request.client_id

            server_info = ServerInfoService().get_server_info()
            webrtc_token = secrets.token_hex(10)

            group_obj = GroupService().get_group_info(group_id)
            group_obj.group_rtc_token = webrtc_token
            group_obj.update()
            # register webrtc
            self.service_group.register_webrtc_token(webrtc_token)
            #  create room
            self.service_group.create_rtc_group(group_id, webrtc_token)
            logger.info('janus webrtc token={}'.format(webrtc_token))
            client_ws_url = get_system_config()['janus_webrtc'].get('client_ws_url')

            # send push notification to all member of group
            lst_client_in_groups = self.service_group.get_clients_in_group(group_id)
            # list token for each device type

            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])

            for client in lst_client_in_groups:
                if client.GroupClientKey.client_workspace_domain != request.from_client_workspace_domain:
                    push_payload = {
                        'notify_type': 'request_call',
                        'call_type': request.call_type,
                        'group_id': str(request.group_id),
                        'group_name': group_obj.group_name if group_obj.group_name else '',
                        'group_type': group_obj.group_type if group_obj.group_type else '',
                        'group_rtc_token': webrtc_token,
                        'group_rtc_url': client_ws_url,
                        'group_rtc_id': str(group_id),
                        'from_client_id': from_client_id,
                        'from_client_name': from_client_name,
                        'from_client_avatar': '',
                        'client_id': client_id,
                        'stun_server': server_info.stun_server,
                        'turn_server': server_info.turn_server
                    }
                    if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                        await NotifyPushService().push_voip_client(client.User.id, push_payload)
                    else:
                        ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.User.id,
                                                                                            json.dumps(push_payload))

            stun_server_obj = json.loads(server_info.stun_server)
            stun_server = video_call_pb2.StunServer(
                server=stun_server_obj["server"],
                port=stun_server_obj["port"]
            )
            turn_server_obj = json.loads(server_info.turn_server)
            turn_server = video_call_pb2.TurnServer(
                server=turn_server_obj["server"],
                port=turn_server_obj["port"],
                type=turn_server_obj["type"],
                user=turn_server_obj["user"],
                pwd=turn_server_obj["pwd"]
            )
            return video_call_pb2.ServerResponse(
                group_rtc_url=client_ws_url,
                group_rtc_id=group_id,
                group_rtc_token=webrtc_token,
                stun_server=stun_server,
                turn_server=turn_server,
            )
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def call_to_group_owner(self, request, group_obj, from_client_id):
        from_client_username = ""
        owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                get_system_config()['grpc_port'])
        group_id = request.group_id
        client_id = request.client_id

        server_info = ServerInfoService().get_server_info()
        webrtc_token = secrets.token_hex(10)

        group_obj.group_rtc_token = webrtc_token
        group_obj.update()
        # register webrtc
        self.service_group.register_webrtc_token(webrtc_token)
        #  create room
        self.service_group.create_rtc_group(group_id, webrtc_token)
        logger.info('janus webrtc token={}'.format(webrtc_token))

        client_ws_url = get_system_config()['janus_webrtc'].get('client_ws_url')

        # send push notification to all member of group
        lst_client_in_groups = self.service_group.get_clients_in_group(group_id)
        # list token for each device type

        for client in lst_client_in_groups:
            if client.User and client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                # if client.GroupClientKey.client_workspace_domain != request.from_client_workspace_domain:
                push_payload = {
                    'notify_type': 'request_call',
                    'call_type': request.call_type,
                    'group_id': str(client.GroupClientKey.group_id),
                    'group_name': group_obj.group_name if group_obj.group_name else '',
                    'group_type': group_obj.group_type if group_obj.group_type else '',
                    'group_rtc_token': webrtc_token,
                    'group_rtc_url':  client_ws_url,
                    'group_rtc_id': str(group_id),
                    'from_client_id': from_client_id,
                    'from_client_name': from_client_username,
                    'from_client_avatar': '',
                    'client_id': client_id,
                    'stun_server': server_info.stun_server,
                    'turn_server': server_info.turn_server
                }
                if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                    await NotifyPushService().push_voip_client(client.User.id, push_payload)
                else:
                    ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.GroupClientKey.client_id,
                                                                                        json.dumps(push_payload))

        stun_server_obj = json.loads(server_info.stun_server)
        stun_server = video_call_pb2.StunServer(
            server=stun_server_obj["server"],
            port=stun_server_obj["port"]
        )
        turn_server_obj = json.loads(server_info.turn_server)
        turn_server = video_call_pb2.TurnServer(
            server=turn_server_obj["server"],
            port=turn_server_obj["port"],
            type=turn_server_obj["type"],
            user=turn_server_obj["user"],
            pwd=turn_server_obj["pwd"]
        )
        return video_call_pb2.ServerResponse(
            group_rtc_url=client_ws_url,
            group_rtc_id=group_id,
            group_rtc_token=webrtc_token,
            stun_server=stun_server,
            turn_server=turn_server
        )

    async def call_to_group_not_owner(self, request, group, from_client_id):
        client_id = request.client_id
        call_type = request.call_type
        from_client_username = ""
        owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                get_system_config()['grpc_port'])
        # request call to owner server, response ọbject push notification
        lst_client = GroupService().get_clients_in_group_owner(group.owner_group_id)
        other_client_in_this_workspace = []
        for client in lst_client:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                client_with_group = {
                    "client_id": client.User.id,
                    "group_id": client.GroupClientKey.group_id
                }
                other_client_in_this_workspace.append(client_with_group)

        request = video_call_pb2.WorkspaceVideoCallRequest(
            from_client_id=from_client_id,
            from_client_name=from_client_username,
            from_client_avatar="",
            from_client_workspace_domain=owner_workspace_domain,
            client_id=client_id,
            group_id=group.owner_group_id,
            call_type=call_type
        )
        obj_res = ClientVideoCall(group.owner_workspace_domain).workspace_video_call(request)
        if obj_res:
            # push for other user in this server
            for client in other_client_in_this_workspace:
                push_payload = {
                    'notify_type': 'request_call',
                    'call_type': call_type,
                    'group_id': str(client["group_id"]),
                    'group_name': group.group_name if group.group_name else '',
                    'group_type': group.group_type if group.group_type else '',
                    'group_rtc_token': obj_res.webrtc_token,
                    'group_rtc_url': obj_res.group_rtc_url,
                    'group_rtc_id': str(obj_res.group_rtc_id),
                    'from_client_id': from_client_id,
                    'from_client_name': from_client_username,
                    'from_client_avatar': '',
                    'client_id': client_id,
                    'stun_server': obj_res.stun_server,
                    'turn_server': obj_res.turn_server
                }
                await self.push_service.push_voip_clients(client.User.id, push_payload)
            return obj_res
        else:
            raise

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
