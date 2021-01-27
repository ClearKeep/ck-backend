import requests
import json
from utils.config import get_system_config
import uuid
from src.models.signal_group_key import GroupClientKey
from src.services.notify_push import NotifyPushService
from src.models.group import GroupChat
from src.services.server_info import ServerInfoService
from protos import video_call_pb2

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
                from_client_username = client.User.username
            else:
                other_clients_in_group.append(client.User.id)

        server_info = ServerInfoService().get_server_info()

        if len(other_clients_in_group) > 0:
            # push notification voip for other clients in group
            push_service = NotifyPushService()
            group_rtc_token = GroupChat().get_group_rtc_token(group_id=group_id)

            push_payload = {
                'notify_type': 'request_call',
                'group_id': str(group_id),
                'group_rtc_token': group_rtc_token.group_rtc_token,
                'from_client_id': from_client_id,
                'from_client_name': from_client_username,
                'from_client_avatar': '',
                'client_id': client_id,
                'stun_server': json.dumps(server_info.stun_server),
                'turn_server': json.dumps(server_info.turn_server)
            }
            push_service.push_voip_clients(other_clients_in_group, push_payload)

        stun_server = video_call_pb2.StunServer(
            server=server_info.turn_server.get("server"),
            port=server_info.turn_server.get("port")
        )

        turn_server = video_call_pb2.TurnServer(
            server=server_info.turn_server.get("server"),
            port=server_info.turn_server.get("port"),
            type=server_info.turn_server.get("type"),
            user=server_info.turn_server.get("user"),
            pwd=server_info.turn_server.get("pwd")
        )

        return video_call_pb2.ServerResponse(
            stun_server=stun_server,
            turn_server=turn_server
        )




