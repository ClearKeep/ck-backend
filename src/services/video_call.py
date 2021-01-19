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
        if group_id:
            lst_client_in_groups = GroupClientKey().get_clients_in_group_with_push_token(group_id)
        elif client_id:
            lst_client_in_groups = User().get_client_id_with_push_token(client_id)
        push_service = NotifyPushService()

        # list token for each device type
        ios_tokens = []
        android_tokens = []
        group_rtc_token = GroupChat().get_group_rtc_token(group_id=group_id)
        for client in lst_client_in_groups:
            if client.User.id == from_client_id:
                from_client_username = client.User.username
            else:
                for client_token in client.User.tokens:
                    if client_token.device_type == DeviceType.android:
                        android_tokens.append(client_token.push_token)
                    elif client_token.device_type == DeviceType.ios:
                        ios_tokens.append(client_token.push_token)

        push_payload = {
            'notify_type': 'request_call',
            'group_id': str(group_id),
            'group_rtc_token': group_rtc_token.group_rtc_token,
            'from_client_id': from_client_id,
            'from_client_name': from_client_username,
            'from_client_avatar': '',
            'client_id': client_id
        }

        if len(android_tokens) > 0:
            push_service.android_data_notification(android_tokens, push_payload)
        if len(ios_tokens) > 0:
            push_service.ios_data_notification(ios_tokens, push_payload)
        # push notification for other clients in group





