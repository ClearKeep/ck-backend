from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.const import DeviceType
from utils.push_notify import *

notify_payload_new_message = messaging.Notification(title='', body='You have a new message')

class NotifyPushService(BaseService):
    def __init__(self):
        super().__init__(NotifyToken())

    def register_token(self, client_id, device_id, device_type, push_token):
        self.model = NotifyToken(
            client_id=client_id,
            device_id=device_id,
            device_type=device_type,
            push_token=push_token,
        )
        return self.model.add()

    def push_text_to_clients(self, lst_client, title, body):
        ios_tokens = []
        android_tokens = []
        push_tokens = self.model.get_clients(lst_client)
        for client_token in push_tokens:
            if client_token.device_type == DeviceType.android:
                android_tokens.append(client_token.push_token)
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                ios_tokens.append(arr_token[-1])

        if len(android_tokens) > 0:
            payload = messaging.Notification(title=title, body=body)
            android_text_notifications(android_tokens, payload)
        if len(ios_tokens) > 0:
            payload_alert = PayloadAlert(title=title, body=body)
            ios_text_notifications(ios_tokens, payload_alert)

    def push_voip_clients(self, lst_client, payload):
        ios_tokens = []
        android_tokens = []
        push_tokens = self.model.get_clients(lst_client)
        for client_token in push_tokens:
            if client_token.device_type == DeviceType.android:
                android_tokens.append(client_token.push_token)
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                ios_tokens.append(arr_token[0])

        if len(android_tokens) > 0:
            android_data_notification(android_tokens, payload)
        if len(ios_tokens) > 0:
            ios_data_notification(ios_tokens, payload)
