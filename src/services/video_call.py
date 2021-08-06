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


class VideoCallService:
    def __init__(self):
        self.service_group = GroupService()
        self.push_service = NotifyPushService()

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


    def update_call(self, update_type, group_id, from_client_id):
        lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
        notify_inapp_service = NotifyInAppService()
        for client in lst_client_in_groups:
            if client.User.id != from_client_id:
                notify_inapp_service.notify_client_update_call(update_type, client.User.id, from_client_id, group_id)

        return video_call_pb2.BaseResponse(
            success=True
        )
