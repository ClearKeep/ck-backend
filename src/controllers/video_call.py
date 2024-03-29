from client.client_push import ClientPush
from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.video_call import VideoCallService
from src.services.group import GroupService
from src.services.server_info import ServerInfoService
from src.services.notify_push import NotifyPushService
from src.services.notify_inapp import NotifyInAppService
from client.client_call import *
import secrets
from utils.config import *
from protos import video_call_pb2
from copy import deepcopy
import logging
import json
logger = logging.getLogger(__name__)

class VideoCallController(BaseController):
    def __init__(self, *kwargs):
        self.service = VideoCallService()
        self.service_group = GroupService()

    @request_logged
    @auth_required
    async def video_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id

            owner_workspace_domain = get_owner_workspace_domain()

            group = GroupService().get_group_info(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                return await self.call_to_group_not_owner(request, group, from_client_id)
            else:
                return await self.call_to_group_owner(request, group, from_client_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_video_call(self, request, context):
        try:
            logger.info("workspace_video_call")

            from_client_id = request.from_client_id
            from_client_name = request.from_client_name
            if request.from_client_avatar:
                from_client_avatar = request.from_client_avatar
            else:
                from_client_avatar = ""
            group_id = request.group_id
            client_id = request.client_id

            server_info = ServerInfoService()
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

            owner_workspace_domain = get_owner_workspace_domain()

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
                        'from_client_avatar': from_client_avatar,
                        'client_id': client_id,
                        'stun_server': json.dumps(server_info.get_stun()),
                        'turn_server': json.dumps(server_info.get_turn())
                    }
                    logger.info(push_payload)
                    if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                        await NotifyPushService().push_voip_client(client.User.id, push_payload)
                    else:
                        new_push_payload = deepcopy(push_payload)
                        new_push_payload['group_id'] = str(client.GroupClientKey.client_workspace_group_id)
                        logger.info(new_push_payload)
                        await ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.User.id,
                                                                                            json.dumps(new_push_payload))

            stun_server = video_call_pb2.StunServer(**server_info.get_stun())

            turn_server = video_call_pb2.TurnServer(**server_info.get_turn())
            return video_call_pb2.ServerResponse(
                group_rtc_url=client_ws_url,
                group_rtc_id=group_id,
                group_rtc_token=webrtc_token,
                stun_server=stun_server,
                turn_server=turn_server,
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_REQUEST_CALL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)


    async def call_to_group_owner(self, request, group_obj, from_client_id):
        from_client_name = ""
        from_client_avatar = ""
        owner_workspace_domain = get_owner_workspace_domain()
        group_id = request.group_id
        logger.info("call_to_group_owner, group_id= {}".format(str(group_id)))

        client_id = request.client_id

        server_info = ServerInfoService()
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
                from_client_name = client.User.display_name
                if client.User.avatar:
                    from_client_avatar = client.User.avatar
                else:
                    from_client_avatar = ""

        for client in lst_client_in_groups:
            if client.User is None or client.User.id != from_client_id:
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
                    'from_client_name': from_client_name,
                    'from_client_avatar': from_client_avatar,
                    'client_id': client_id,
                    'stun_server': json.dumps(server_info.get_stun()),
                    'turn_server': json.dumps(server_info.get_turn())
                }
                logger.info(push_payload)

                if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                    await NotifyPushService().push_voip_client(client.User.id, push_payload)
                else:
                    logger.info("Push voip from {} to client {} in {}".format(owner_workspace_domain, client.GroupClientKey.client_workspace_domain, client.GroupClientKey.client_id))
                    new_push_payload = deepcopy(push_payload)
                    new_push_payload['group_id'] = str(client.GroupClientKey.client_workspace_group_id)
                    logger.info(new_push_payload)
                    await ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.GroupClientKey.client_id,
                                                                                        json.dumps(new_push_payload))

        stun_server = video_call_pb2.StunServer(**server_info.get_stun())
        turn_server = video_call_pb2.TurnServer(**server_info.get_turn())
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
        from_client_name = ""
        from_client_avatar = ""
        owner_workspace_domain = get_owner_workspace_domain()

        logger.info("call_to_group_not_owner, group_id={}".format(str(group.id)))

        # request call to owner server, response ọbject push notification
        lst_client = GroupService().get_clients_in_group_owner(group.owner_group_id)

        for client in lst_client:
            if client.User and client.User.id == from_client_id:
                from_client_name = client.User.display_name
                if client.User.avatar:
                    from_client_avatar = client.User.avatar
                else:
                    from_client_avatar = ""

        other_client_in_this_workspace = []
        for client in lst_client:
            if client.User and client.User.id != from_client_id:
                client_with_group = {
                    "client_id": client.User.id,
                    "group_id": client.GroupClientKey.group_id
                }
                other_client_in_this_workspace.append(client_with_group)

        request = video_call_pb2.WorkspaceVideoCallRequest(
            from_client_id=from_client_id,
            from_client_name=from_client_name,
            from_client_avatar=from_client_avatar,
            from_client_workspace_domain=owner_workspace_domain,
            client_id=client_id,
            group_id=group.owner_group_id,
            call_type=call_type
        )
        obj_res = await ClientVideoCall(group.owner_workspace_domain).workspace_video_call(request)
        if obj_res:
            # push for other user in this server
            for client in other_client_in_this_workspace:
                push_payload = {
                    'notify_type': 'request_call',
                    'call_type': call_type,
                    'group_id': str(client["group_id"]),
                    'group_name': group.group_name if group.group_name else '',
                    'group_type': group.group_type if group.group_type else '',
                    'group_rtc_token': obj_res.group_rtc_token,
                    'group_rtc_url': obj_res.group_rtc_url,
                    'group_rtc_id': str(obj_res.group_rtc_id),
                    'from_client_id': from_client_id,
                    'from_client_name': from_client_name,
                    'from_client_avatar': from_client_avatar,
                    'client_id': client_id,
                    'stun_server': obj_res.stun_server,
                    'turn_server': obj_res.turn_server
                }
                logger.info(push_payload)
                await NotifyPushService().push_voip_client(client["client_id"], push_payload)
            return obj_res
        else:
            raise

    @request_logged
    @auth_required
    async def update_call(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            from_client_id = introspect_token['sub']
            group_id = request.group_id

            owner_workspace_domain = get_owner_workspace_domain()

            group = GroupService().get_group_info(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                return await self.update_call_to_group_not_owner(request, group, from_client_id)
            else:
                return await self.update_call_to_group_owner(request, from_client_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_UPDATE_CALL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_update_call(self, request, context):
        try:
            logger.info("workspace_update_call")

            from_client_id = request.from_client_id
            from_client_name = request.from_client_name
            from_client_avatar = request.from_client_avatar
            group_id = request.group_id
            client_id = request.client_id
            update_type = request.update_type

            # send push notification to all member of group
            lst_client_in_groups = self.service_group.get_clients_in_group(group_id)
            # list token for each device type
            owner_workspace_domain = get_owner_workspace_domain()

            for client in lst_client_in_groups:
                if client.GroupClientKey.client_workspace_domain != request.from_client_workspace_domain:
                    push_payload = {
                        'notify_type': update_type,
                        'group_id': str(client.GroupClientKey.group_id),
                        'from_client_id': from_client_id,
                        'from_client_name': from_client_name,
                        'from_client_avatar': from_client_avatar if from_client_avatar else "",
                        'client_id': client_id
                    }
                    if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                        # ret_val = NotifyInAppService().notify_client_update_call(update_type, client.GroupClientKey.client_id, from_client_id,
                        #                                                          client.GroupClientKey.group_id)
                        # if not ret_val:
                        new_push_payload = deepcopy(push_payload)
                        logger.info(new_push_payload)
                        await NotifyPushService().push_voip_client(client.GroupClientKey.client_id, new_push_payload)
                    else:
                        new_push_payload = deepcopy(push_payload)
                        new_push_payload["group_id"] = str(client.GroupClientKey.client_workspace_group_id)
                        logger.info(new_push_payload)
                        await ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.GroupClientKey.client_id,
                                                                                            json.dumps(new_push_payload))
                        #continue
            return video_call_pb2.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_UPDATE_CALL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def update_call_to_group_owner(self, request, from_client_id):
        logger.info("update_call_to_group_owner")

        from_client_name = ""
        from_client_avatar = ""
        owner_workspace_domain = get_owner_workspace_domain()

        group_id = request.group_id
        client_id = request.client_id
        update_type = request.update_type

        # send push notification to all member of group
        lst_client_in_groups = self.service_group.get_clients_in_group(group_id)

        for client in lst_client_in_groups:
            if client.User and client.User.id == from_client_id:
                from_client_name = client.User.display_name
                from_client_avatar = client.User.avatar

        for client in lst_client_in_groups:
            push_payload = {
                'notify_type': update_type,
                'group_id': str(client.GroupClientKey.group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_name,
                'from_client_avatar': from_client_avatar if from_client_avatar else "",
                'client_id': client_id
            }
            if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                # logger.info("update_call_to_group_owner, owner member ->client_id {}".format(client.GroupClientKey.client_id))
                # ret_val = NotifyInAppService().notify_client_update_call(update_type, client.GroupClientKey.client_id, from_client_id,
                #                                                          client.GroupClientKey.group_id)
                # logger.info("notify inapp {}".format(ret_val))
                # if not ret_val:
                #     logger.info("notify push notification")
                new_push_payload = deepcopy(push_payload)
                new_push_payload["group_id"] = str(client.GroupClientKey.group_id)
                logger.info(new_push_payload)
                await NotifyPushService().push_voip_client(client.GroupClientKey.client_id, new_push_payload)
            else:
                new_push_payload = deepcopy(push_payload)
                new_push_payload["group_id"] = str(client.GroupClientKey.client_workspace_group_id)
                logger.info(new_push_payload)
                await ClientPush(client.GroupClientKey.client_workspace_domain).push_voip(client.GroupClientKey.client_id,
                                                                                    json.dumps(new_push_payload))
                #continue

        return video_call_pb2.BaseResponse()

    async def update_call_to_group_not_owner(self, request, group, from_client_id):
        logger.info("update_call_to_group_not_owner")

        client_id = request.client_id
        update_type = request.update_type
        from_client_username = ""
        from_client_avatar = ""
        owner_workspace_domain = get_owner_workspace_domain()

        # update call to owner server, response ọbject push notification
        lst_client = GroupService().get_clients_in_group_owner(group.owner_group_id)
        for client in lst_client:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
                from_client_avatar = client.User.avatar
                break

        for client in lst_client:
            push_payload = {
                'notify_type': update_type,
                'group_id': str(client.GroupClientKey.group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': from_client_avatar if from_client_avatar else "",
                'client_id': client_id
            }
            await NotifyPushService().push_voip_client(client.GroupClientKey.client_id, push_payload)

        request = video_call_pb2.WorkspaceUpdateCallRequest(
            from_client_id=from_client_id,
            from_client_name=from_client_username,
            from_client_avatar=from_client_avatar,
            from_client_workspace_domain=owner_workspace_domain,
            client_id=client_id,
            group_id=group.owner_group_id,
            update_type=update_type
        )
        await ClientVideoCall(group.owner_workspace_domain).workspace_update_call(request)
        return video_call_pb2.BaseResponse()
