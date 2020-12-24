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
        # send push notification to all member of group
        lst_client_in_groups = GroupClientKey().get_clients_in_group_with_push_token(group_id)
        push_service = NotifyPushService()
        android_payload = {
            'notify_type': 'request_call',
            'group_id': str(group_id),
            'from_client_id': from_client_id,
            'from_client_name': from_client_username,
            'from_client_avatar': '',
            'client_id': client_id
        }
        ios_payload = {
           'aps' : {
              'alert' : {
                 'title' : 'request_call',
                 'subtitle' : 'request_call',
                 'body' : 'call',
                        },
              'category' : 'request_call'
                    },
           'gameID' : '12345678'
        }
        for client in lst_client_in_groups:
            ios_tokens = []
            android_tokens = []
            if client.client_id == from_client_id:
                from_client_username = client.User.username
            else:
                for client_token in client.User.tokens:
                    if client_token.device_type == 'android':
                        android_tokens.append(client_token.push_token)
                    elif client_token.device_type == 'ios':
                        push_service.ios_data_notification(client_token.push_token, ios_payload)

            if len(android_tokens) > 0:
                push_service.android_data_notification(android_tokens, android_payload)
        # push notification for other clients in group





