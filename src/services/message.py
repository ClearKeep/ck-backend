from src.services.base import BaseService
from src.models.message import Message
from src.models.group import GroupChat
from src.models.message_user_read import MessageUserRead
from protos import message_pb2
from threading import Thread
from datetime import datetime
from queue import Queue
import uuid
import asyncio
from utils.config import *
from utils.logger import *

client_message_queue = {}
import logging
logger = logging.getLogger(__name__)

class MessageService(BaseService):
    """
    MessageService, involved in storing new message, updating message, loading message history, subscribe/unsubcribe message channel for user
    """
    def __init__(self):
        super().__init__(Message())
        self.service_group = GroupChat()
        self.message_read_model = MessageUserRead()

    def store_message(self, message_id, created_at, group_id, group_type, from_client_id, from_client_workspace_domain, client_id, message, sender_message=b''):
        # init new message
        self.model = Message(
            id=message_id,
            group_id=group_id,
            from_client_id=from_client_id,
            from_client_workspace_domain=from_client_workspace_domain,
            client_id=client_id,
            message=message,
            created_at=created_at,
            sender_message=sender_message
        )
        self.model.add()
        self.update_group_last_message(group_id, created_at, message_id)
        # response
        new_message = self.model.get(message_id)
        res_obj = message_pb2.MessageObjectResponse(
            id=new_message.id,
            group_id=new_message.group_id,
            group_type=group_type,
            from_client_id=new_message.from_client_id,
            from_client_workspace_domain=new_message.from_client_workspace_domain,
            message=message,
            created_at=int(new_message.created_at.timestamp() * 1000),
            sender_message=sender_message
        )
        if new_message.client_id:
            res_obj.client_id = new_message.client_id
        if new_message.updated_at:
            res_obj.updated_at = int(new_message.updated_at.timestamp() * 1000)

        res_obj.client_workspace_domain = get_owner_workspace_domain()

        return res_obj

    def update_group_last_message(self, group_id, created_at, message_id):
        GroupChat(
            id=group_id,
            last_message_at=created_at,
            last_message_id=message_id
        ).update()


    def update_message(
            self,
            group_id,
            from_client_id,
            client_id,
            message,
            message_id):
        self.model = Message().get(message_id)
        updated_at = datetime.now()
        self.model.updated_at = updated_at
        self.model.update()
        edited_message = self.model
        res_obj = message_pb2.MessageObjectResponse(
            id=edited_message.id,
            group_id=edited_message.group_id,
            from_client_id=edited_message.from_client_id,
            message=message,
            created_at=int(edited_message.created_at.timestamp() * 1000)
        )
        if edited_message.client_id:
            res_obj.client_id = edited_message.client_id
        if edited_message.updated_at:
            res_obj.updated_at = int(edited_message.updated_at.timestamp() * 1000)

        if client_id:
            res_obj.group_type = "peer"
        else:
            res_obj.group_type = "group"

        return res_obj

    def get_message_in_group(self, client_id, group_id, offset=0, from_time=0):
        lst_message = self.model.get_message_in_group(group_id, offset, from_time)
        group_type = self.service_group.get_group_type(group_id=group_id)
        lst_obj_res = []
        for obj in lst_message:
            obj_res = message_pb2.MessageObjectResponse(
                id=obj.id,
                group_id=obj.group_id,
                group_type=group_type.group_type,
                from_client_id=obj.from_client_id,
                from_client_workspace_domain=obj.from_client_workspace_domain,
                message=obj.message,
                created_at=int(obj.created_at.timestamp() * 1000),
            )
            if obj.from_client_id == client_id:
                obj_res.sender_message = obj.sender_message
            if obj.client_id:
                obj_res.client_id = obj.client_id
            if obj.updated_at is not None:
                obj_res.updated_at = int(obj.updated_at.timestamp() * 1000)

            for client_read_item in obj.users_read:
                client_read = message_pb2.ClientReadObject(
                    id=client_read_item.user.id,
                    display_name=client_read_item.user.display_name,
                    avatar=client_read_item.user.avatar
                )
                obj_res.lst_client_read.append(client_read)

            lst_obj_res.append(obj_res)

        response = message_pb2.GetMessagesInGroupResponse(
            lst_message=lst_obj_res
        )
        return response

    async def subscribe(self, client_id, device_id):
        message_channel = "message/{}/{}".format(client_id, device_id)
        logger.info(f"subscribe message channel {message_channel}")
        if message_channel in client_message_queue:
            client_message_queue[message_channel] = None
            del client_message_queue[message_channel]
            await asyncio.sleep(1)
        client_message_queue[message_channel] = Queue()

    def un_subscribe(self, client_id, device_id):
        message_channel = "message/{}/{}".format(client_id, device_id)
        logger.info(f"unsubscribe message channel {message_channel}")
        if message_channel in client_message_queue:
            client_message_queue[message_channel] = None
            del client_message_queue[message_channel]

    def read_messages(self, client_id, lst_message_id):
        for mess_id in lst_message_id:
            MessageUserRead(
                message_id=mess_id,
                client_id=client_id
            ).add()
