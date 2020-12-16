import requests
import json
from utils.config import get_system_config
import uuid
from src.models.signal_group_key import GroupClientKey
from src.services.notify_push import NotifyPushService


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
        list_client_push_token = []

        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group_with_push_token(group_id)

        for client in lst_client_in_groups:
            if client.client_id == from_client_id:
                from_client_username = client.username
            else:
                for client_token in client.NotifyToken:
                    list_client_push_token.append(client_token.push_token)
        # push notification for other clients in group
        push_service = NotifyPushService()
        push_payload = {
            "group_id": group_id,
            "from_client": {
                "client_id": from_client_id,
                "username": from_client_username,
                "avatar": ""
            },
            "client_id": client_id
        }
        push_service.android_data_notification(list_client_push_token, push_payload)

