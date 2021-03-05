import requests
import json
from utils.config import get_system_config
import uuid
from src.models.signal_group_key import GroupClientKey
from src.services.notify_push import NotifyPushService
from src.models.group import GroupChat
from src.services.server_info import ServerInfoService
from protos import video_call_pb2
from src.services.group import GroupService
import secrets
from utils.logger import *

class VideoCallService:
    def __init__(self):
        pass

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

    def request_call(self, group_id, from_client_id, client_id):
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
        rtc_token = GroupService().register_webrtc_token(webrtc_token)
        group_janus_room_url = GroupService.get_url_janus_create_room(group_id=group_id)
        # check create room
        room_rtc = GroupService().check_rtc_room(room_id=group_id,janus_check_room_url=group_janus_room_url,rtc_token=rtc_token)
        if room_rtc == None:
            GroupService().create_rtc_group(group_id, rtc_token)
        logger.info('janus webrtc token={}'.format(webrtc_token))

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            push_payload = {
                'notify_type': 'request_call',
                'group_id': str(group_id),
                'group_rtc_token': webrtc_token,
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id,
                'stun_server': server_info.stun_server,
                'turn_server': server_info.turn_server
            }
            push_service.push_voip_clients(other_clients_in_group, push_payload,from_client_id)

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
            group_rtc_token=webrtc_token
        )

    def cancel_request_call(self, group_id, from_client_id, client_id):
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
            push_service.push_voip_clients(other_clients_in_group, push_payload, from_client_id)
        return video_call_pb2.BaseResponse(
            success=True
        )

