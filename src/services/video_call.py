import requests
import json
from utils.config import get_system_config
import uuid
from src.models.signal_group_key import GroupClientKey
from src.models.video_call import VideoCall
from src.models.message import Message
from src.services.notify_push import NotifyPushService
from src.services.server_info import ServerInfoService
from src.services.notify_inapp import NotifyInAppService
from protos import video_call_pb2
from src.services.group import GroupService
import secrets
from utils.logger import *


class VideoCallService:
    def __init__(self):
        self.service_group = GroupService()

    def add_client_token(self, token):
        webrtc_config = get_system_config()["janus_webrtc"]
        transaction = str(uuid.uuid4()).replace("-", "")
        payload = {
            "janus": "add_token",
            "token": token,
            "transaction": transaction,
            "admin_secret": webrtc_config["admin_secret"]
        }
        response = requests.post(webrtc_config["server_url"], payload)
        if response["janus"] == "success":
            return True
        else:
            return False

    def remove_client_token(self, token):
        webrtc_config = get_system_config()["janus_webrtc"]
        transaction = str(uuid.uuid4()).replace("-", "")
        payload = {
            "janus": "remove_token",
            "token": token,
            "transaction": transaction,
            "admin_secret": webrtc_config["admin_secret"]
        }
        response = requests.post(webrtc_config["server_url"], payload)
        if response["janus"] == "success":
            return True
        else:
            return False

    async def request_call(self, call_type, group_id, from_client_id, client_id):
        from_client_username = ""
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        # list token for each device type
        other_clients_in_group = []
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                other_clients_in_group.append(client.User.id)

        server_info = ServerInfoService().get_server_info()

        webrtc_token = secrets.token_hex(10)

        group_obj = self.service_group.get_group_obj(group_id=group_id)
        group_obj.group_rtc_token = webrtc_token
        group_obj.update()
        # register webrtc
        self.service_group.register_webrtc_token(webrtc_token)
        #  create room
        self.service_group.create_rtc_group(group_id, webrtc_token)
        logger.info('janus webrtc token={}'.format(webrtc_token))

        video_call = VideoCall(
            id=str(uuid.uuid4()),
            call_status='call_created',
            call_type=call_type,
            created_at=datetime.now()
        )
        if len(other_clients_in_group) > 2:
            video_call.started_at = video_call.created_at
        message = Message(
            id=str(uuid.uuid4()),
            group_id=group_id,
            from_client_id=from_client_id,
            client_id=client_id,
            message=video_call.id,
            message_type='call_status',
            created_at=video_call.created_at
        )
        video_call.message_id=message.id
        video_call.add()
        res_obj = video_call_pb2.VideoCallMessage(
            id=video_call.id,
            message_id=message.id,
            call_status=video_call.call_status,
            call_type=video_call.call_type,
            created_at=int(video_call.created_at.timestamp() * 1000),
            started_at=int(video_call.started_at.timestamp() * 1000),
            ended_at=int(video_call.ended_at.timestamp() * 1000)
        )

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'request_call',
                'call_type': call_type,
                'group_id': str(group_id),
                'group_name': group_obj.group_name if group_obj.group_name else '',
                'group_type': group_obj.group_type if group_obj.group_type else '',
                'group_rtc_token': webrtc_token,
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id,
                'stun_server': server_info.stun_server,
                'turn_server': server_info.turn_server
            }

            await push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)

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
            stun_server=stun_server,
            turn_server=turn_server,
            group_rtc_token=webrtc_token,
            video_call=res_obj
        )

    async def cancel_request_call(self, group_id, from_client_id, client_id,
                                  call_id):
        video_call = VideoCall().get(call_id=call_id)
        video_call.call_status = 'call_missed'
        video_call.ended_at = datetime.now()
        res_obj = video_call_pb2.VideoCallMessage(
            id=video_call.id,
            message_id=video_call.message_id,
            call_status=video_call.call_status,
            call_type=video_call.call_type,
            created_at=int(video_call.created_at.timestamp() * 1000),
            started_at=int(video_call.started_at.timestamp() * 1000),
            ended_at=int(video_call.ended_at.timestamp() * 1000)
        )
        video_call.update()
        from_client_username = ""
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        # list token for each device type
        other_clients_in_group = []
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                other_clients_in_group.append(client.User.id)

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'cancel_request_call',
                'group_id': str(group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id
            }
            await push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)
        return video_call_pb2.VideoCallResponse(
            group_id=group_id,
            from_client_id=from_client_id,
            client_id=client_id,
            video_call=res_obj
        )

    async def miss_call(self, group_id, from_client_id, client_id, call_id):
        video_call = VideoCall().get(call_id=call_id)
        video_call.call_status = 'call_missed'
        video_call.ended_at = datetime.now()
        res_obj = video_call_pb2.VideoCallMessage(
            id=video_call.id,
            message_id=video_call.message_id,
            call_status=video_call.call_status,
            call_type=video_call.call_type,
            created_at=int(video_call.created_at.timestamp() * 1000),
            started_at=int(video_call.started_at.timestamp() * 1000),
            ended_at=int(video_call.ended_at.timestamp() * 1000)
        )
        video_call.update()
        from_client_username = ""
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        # list token for each device type
        other_clients_in_group = []
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                other_clients_in_group.append(client.User.id)

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'miss_call',
                'group_id': str(group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id
            }
            await push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)
        return video_call_pb2.VideoCallResponse(
            group_id=group_id,
            from_client_id=from_client_id,
            client_id=client_id,
            video_call=res_obj
        )

    async def decline_call(self, group_id, from_client_id, client_id, call_id):
        video_call = VideoCall().get(call_id=call_id)
        video_call.call_status = 'call_declined'
        video_call.ended_at = datetime.now()
        res_obj = video_call_pb2.VideoCallMessage(
            id=video_call.id,
            message_id=video_call.message_id,
            call_status=video_call.call_status,
            call_type=video_call.call_type,
            created_at=int(video_call.created_at.timestamp() * 1000),
            started_at=int(video_call.started_at.timestamp() * 1000),
            ended_at=int(video_call.ended_at.timestamp() * 1000)
        )
        video_call.update()
        from_client_username = ""
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        # list token for each device type
        other_clients_in_group = []
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                other_clients_in_group.append(client.User.id)

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'decline_call',
                'group_id': str(group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id
            }
            await push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)
        return video_call_pb2.VideoCallResponse(
            group_id=group_id,
            from_client_id=from_client_id,
            client_id=client_id,
            video_call=res_obj
        )

    async def end_call(self, group_id, from_client_id, client_id, call_id):
        video_call = VideoCall().get(call_id=call_id)
        video_call.call_status = 'call_ended'
        video_call.ended_at = datetime.now()
        res_obj = video_call_pb2.VideoCallMessage(
            id=video_call.id,
            message_id=video_call.message_id,
            call_status=video_call.call_status,
            call_type=video_call.call_type,
            created_at=int(video_call.created_at.timestamp() * 1000),
            started_at=int(video_call.started_at.timestamp() * 1000),
            ended_at=int(video_call.ended_at.timestamp() * 1000)
        )
        from_client_username = ""
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        # list token for each device type
        other_clients_in_group = []
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.display_name
            else:
                other_clients_in_group.append(client.User.id)

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'end_call',
                'group_id': str(group_id),
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id
            }
            await push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)
        return video_call_pb2.VideoCallResponse(
            group_id=group_id,
            from_client_id=from_client_id,
            client_id=client_id,
            video_call=res_obj
        )

    def update_call(self, update_type, group_id, from_client_id):
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        notify_inapp_service = NotifyInAppService()
        for client in lst_client_in_groups:
            if client.User.id != from_client_id:
                notify_inapp_service.notify_client_update_call(update_type, client.User.id, from_client_id, group_id)

        return video_call_pb2.BaseResponse(
            success=True
        )
