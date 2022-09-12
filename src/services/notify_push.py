import asyncio
from enum import Enum, unique

from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.const import DeviceType
from utils.push_notify import *
from msg.message import Message
from utils.logger import *
from utils.config import *

import logging
logger = logging.getLogger(__name__)


class PushType(Enum):
    DEACTIVE_ACCOUNT = 'deactive_account'
    RESET_PINCODE = 'reset_pincode'


class NotifyPushService(BaseService):
    """
    Notify push service, using for pushing notification to client_id when he/her not log in

    """
    def __init__(self):
        super().__init__(NotifyToken())

    def register_token(self, client_id, device_id, device_type, push_token, end_user_env):
        # register push_token for device_id of client_id want to get notification not online
        try:
            self.model = NotifyToken(
                client_id=client_id,
                device_id=device_id,
                device_type=device_type,
                push_token=push_token,
                end_user_env=end_user_env
            )
            return self.model.add()
        except Exception as e:
            logger.info(e)
            raise Exception(Message.REGISTER_USER_FAILED)

    def delete_token(self, client_id, device_id):
        # delete push_token for device_id of client_id
        try:
            id_device_token = self.model.get(client_id=client_id, device_id=device_id)
            if id_device_token:
                id_device_token.delete()
            else:
                raise Exception(Message.UNAUTHENTICATED)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.UNAUTHENTICATED)

    async def push_text_to_client_with_device(self, to_client_id, to_device_id, title, body, from_client_id, notify_type, data, from_client_device_id=None):
        # push text to specific to_device_id of to_client_id with remained info
        logger.info('push_text_to_client')
        client_token = self.model.get(to_client_id, to_device_id)
        if client_token.device_id != from_client_device_id:
            if client_token.device_type == DeviceType.android:
                push_payload = {
                    'title': title,
                    'body': body,
                    'client_id': client_token.client_id,
                    'client_workspace_domain': get_owner_workspace_domain(),
                    'notify_type': notify_type,
                    'data': data
                }
                await android_data_notification(client_token.push_token, push_payload, client_token.end_user_env)
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                push_payload = {
                    'title': title,
                    'body': body
                }
                await ios_text_notifications(arr_token[-1], push_payload, data, client_token.end_user_env)

    async def push_text_to_client(self, to_client_id, title, body, from_client_id, notify_type, data, from_client_device_id=None):
        # push text to all device of to_client_id with remained info
        logger.info('push_text_to_client')
        client_tokens = self.model.get_client_device_ids(to_client_id)

        awaitables = []
        for client_token in client_tokens:
            if client_token.device_id == from_client_device_id:
                continue
            if client_token.device_type == DeviceType.android:
                push_payload = {
                    'title': title,
                    'body': body,
                    'client_id': client_token.client_id,
                    'client_workspace_domain': get_owner_workspace_domain(),
                    'notify_type': notify_type,
                    'data': data
                }
                awaitables.append(android_data_notification(client_token.push_token, push_payload, client_token.end_user_env))
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                push_payload = {
                    'title': title,
                    'body': body
                }
                awaitables.append(ios_text_notifications(arr_token[-1], push_payload, data, client_token.end_user_env))

        await asyncio.gather(*awaitables)

    async def push_text_to_clients(self, lst_client, title, body, from_client_id, notify_type, data):
        # push text to all device of list clients with remained info
        client_device_push_tokens = self.model.get_clients(lst_client)
        awaitables = []
        for client_token in client_device_push_tokens:
            if client_token.device_type == DeviceType.android:
                push_payload = {
                    'title': title,
                    'body': body,
                    'client_id': client_token.client_id,
                    'client_workspace_domain': get_owner_workspace_domain(),
                    'notify_type': notify_type,
                    'data': data
                }
                awaitables.append(android_data_notification(client_token.push_token, push_payload, client_token.end_user_env))
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                push_payload = {
                    'title': title,
                    'body': body
                }
                awaitables.append(ios_text_notifications(arr_token[-1], push_payload, data, client_token.end_user_env))
        await asyncio.gather(*awaitables)


    async def push_voip_client(self, to_client_id, payload):
        # push payload to all device of to_client_id without any addition info
        client_tokens = self.model.get_client_device_ids(to_client_id)
        awaitables = []
        for client_token in client_tokens:
            payload['client_id'] = client_token.client_id
            payload['client_workspace_domain'] = get_owner_workspace_domain()
            if client_token.device_type == DeviceType.android:
                awaitables.append(android_data_notification(client_token.push_token, payload, client_token.end_user_env))
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                awaitables.append(ios_data_notification(arr_token[0], payload, client_token.end_user_env))
        await asyncio.gather(*awaitables)

    async def push_voip_clients(self, lst_client, payload, from_client_id):
        # push payload to all device of lst_client with infor about from_client_id
        client_device_push_tokens = self.model.get_clients(lst_client)
        awaitables = []
        for client_token in client_device_push_tokens:
            payload['client_id'] = client_token.client_id
            payload['client_workspace_domain'] = get_owner_workspace_domain()
            if client_token.device_type == DeviceType.android:
                awaitables.append(android_data_notification(client_token.push_token, payload))
            elif client_token.device_type == DeviceType.ios:
                arr_token = client_token.push_token.split(',')
                awaitables.append(ios_data_notification(arr_token[0], payload))
        await asyncio.gather(*awaitables)
