from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.const import DeviceType
from utils.push_notify import *
from msg.message import Message
from utils.logger import *
from utils.config import *


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

    async def push_text_to_client(self, to_client_id, title, body, from_client_id, notify_type, data):
        client_tokens = self.model.get_client(to_client_id)
        if len(client_tokens) == 0:
            return
        client_token = client_tokens[0]
        from_client_devices = self.model.get_client(from_client_id)
        if len(from_client_devices) > 0 and client_token.device_id == from_client_devices[0].device_id:
            return
        try:
            if client_token.device_type == DeviceType.android:
                push_payload = {
                    'title': title,
                    'body': body,
                    'client_id': client_token.client_id,
                    'client_workspace_domain': get_owner_workspace_domain(),
                    'notify_type': notify_type,
                    'data': data
                }
                android_data_notification(client_token.push_token, push_payload)
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                push_payload = {
                    'title': title,
                    'body': body
                }
                await ios_text_notifications(arr_token[-1], push_payload)
        except Exception as e:
            logger.error(e)

    async def push_text_to_clients(self, lst_client, title, body, from_client_id, notify_type, data):
        client_device_push_tokens = self.model.get_clients(lst_client)
        # from_client_devices = self.model.get_client(from_client_id)
        for client_token in client_device_push_tokens:
            # if len(from_client_devices) > 0 and client_token.device_id == from_client_devices[0].device_id:
            #     continue
            # else:
            try:
                if client_token.device_type == DeviceType.android:
                    push_payload = {
                        'title': title,
                        'body': body,
                        'client_id': client_token.client_id,
                        'client_workspace_domain': get_owner_workspace_domain(),
                        'notify_type': notify_type,
                        'data': data
                    }
                    android_data_notification(client_token.push_token, push_payload)
                elif client_token.device_type == DeviceType.ios:
                    arr_token = client_token.push_token.split(',')
                    push_payload = {
                        'title': title,
                        'body': body
                    }
                    await ios_text_notifications(arr_token[-1], push_payload)
            except Exception as e:
                # client_token.delete()
                continue

    async def push_voip_client(self, to_client_id, payload):
        client_tokens = self.model.get_client(to_client_id)
        if len(client_tokens) > 0:
            client_token = client_tokens[0]
            try:
                payload['client_id'] = client_token.client_id
                payload['client_workspace_domain'] = get_owner_workspace_domain()

                if client_token.device_type == DeviceType.android:
                    android_data_notification(client_token.push_token, payload)
                elif client_token.device_type == DeviceType.ios:
                    arr_token = client_token.push_token.split(',')
                    await ios_data_notification(arr_token[0], payload)
            except Exception as e:
                logger.error(e)

    async def push_voip_clients(self, lst_client, payload, from_client_id):
        # ios_tokens = []
        # android_tokens = []
        # from_client_devices = self.model.get_client(from_client_id)
        client_device_push_tokens = self.model.get_clients(lst_client)
        for client_token in client_device_push_tokens:
            # if len(from_client_devices) > 0 and client_token.device_id == from_client_devices[0].device_id:
            #     continue
            # else:
            try:
                payload['client_id'] = client_token.client_id
                payload['client_workspace_domain'] = get_owner_workspace_domain()
                if client_token.device_type == DeviceType.android:
                    android_data_notification(client_token.push_token, payload)
                elif client_token.device_type == DeviceType.ios:
                    arr_token = client_token.push_token.split(',')
                    await ios_data_notification(arr_token[0], payload)
            except Exception as e:
                # client_token.delete()
                continue
