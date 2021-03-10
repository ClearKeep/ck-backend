from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.const import DeviceType
from utils.push_notify import *
from msg.message import Message
from utils.logger import *


class NotifyPushService(BaseService):
    def __init__(self):
        super().__init__(NotifyToken())

    def register_token(self, client_id, device_id, device_type, push_token):
        try:
            self.model = NotifyToken(
                client_id=client_id,
                device_id=device_id,
                device_type=device_type,
                push_token=push_token,
            )
            return self.model.add()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def delete_token(self, client_id, device_id):
        try:
            id_device_token = self.model.get(client_id=client_id, device_id=device_id)
            if id_device_token:
                id_device_token.delete()
            else:
                raise Exception(Message.UNAUTHENTICATED)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    async def push_text_to_clients(self, lst_client, title, body, from_client_id):
        ios_tokens = []
        android_tokens = []
        client_device_push_tokens = self.model.get_clients(lst_client)
        from_client_devices = self.model.get_client(from_client_id)
        for client_token in client_device_push_tokens:
            if client_token.device_id != from_client_devices[0].device_id:
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
            await ios_text_notifications(ios_tokens, payload_alert)

    async def push_voip_clients(self, lst_client, payload, from_client_id):
        ios_tokens = []
        android_tokens = []
        from_client_devices = self.model.get_client(from_client_id)
        client_device_push_tokens = self.model.get_clients(lst_client)
        for client_token in client_device_push_tokens:
            if client_token.device_id != from_client_devices[0].device_id:
                if client_token.device_type == DeviceType.android:
                    android_tokens.append(client_token.push_token)
                elif client_token.device_type == DeviceType.ios:
                    arr_token = client_token.push_token.split(',')
                    ios_tokens.append(arr_token[0])
            else:
                self.delete_token(client_token.client_id, client_token.device_id)

        if len(android_tokens) > 0:
            android_data_notification(android_tokens, payload)
        if len(ios_tokens) > 0:
            await ios_data_notification(ios_tokens, payload)
