import requests
import json
from utils.config import get_system_config
from utils.const import DeviceType
import uuid
from src.models.signal_group_key import GroupClientKey
from src.models.user import User
from src.services.notify_push import NotifyPushService
from src.models.group import GroupChat

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
                'client_id': client_id
            }
            push_service.push_voip_clients(other_clients_in_group, push_payload)






