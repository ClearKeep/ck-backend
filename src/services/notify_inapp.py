from src.services.base import BaseService
from src.models.notify import Notify
from protos import notify_pb2
from queue import Queue
from middlewares.request_logged import *
import asyncio
from datetime import datetime

# notify type
NEW_PEER = "new-peer"
IN_PEER = "in-peer"
NEW_GROUP = "new-group"
IN_GROUP = "in-group"
PEER_UPDATE_SIGNAL_KEY = "peer-update-key"
UPDATE_CALL = "update-call"

client_notify_queue = {}

class NotifyInAppService(BaseService):
    def __init__(self):
        super().__init__(Notify())

    def get_unread_notifies(self, client_id):
        lst_notify = self.model.get_unread_notifies(client_id)
        lst_obj_res = []
        for obj in lst_notify:
            obj_res = notify_pb2.NotifyObjectResponse (
                id=obj.id,
                client_id=obj.client_id,
                notify_type=obj.notify_type,
                read_flg=obj.read_flg,
                created_at=int(obj.created_at.timestamp() * 1000)
            )
            if obj.ref_client_id:
                obj_res.ref_client_id = obj.ref_client_id
            if obj.ref_group_id:
                obj_res.ref_group_id = obj.ref_group_id
            if obj.ref_group_id:
                obj_res.ref_group_id = obj.ref_group_id
            if obj.notify_image:
                obj_res.notify_image = obj.notify_image
            if obj.notify_title:
                obj_res.notify_title = obj.notify_title
            if obj.notify_content:
                obj_res.notify_content = obj.notify_content

            lst_obj_res.append(obj_res)

        response = notify_pb2.GetNotifiesResponse(
            lst_message=lst_obj_res
        )
        return response

    async def subscribe(self, client_id):
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            client_notify_queue[notify_channel] = None
            del client_notify_queue[notify_channel]
            await asyncio.sleep(1)
        client_notify_queue[notify_channel] = Queue()


    def un_subscribe(self, client_id):
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            client_notify_queue[notify_channel] = None
            del client_notify_queue[notify_channel]

    def read_notify(self, notify_id):
        self.model = Notify(id=notify_id, read_flg=True)
        self.model.update()

    # add notify
    def notify_invite_peer(self, client_id, ref_client_id, ref_group_id):
        self.model = Notify(
            client_id=client_id,
            ref_client_id=ref_client_id,
            ref_group_id=ref_group_id,
            notify_type=NEW_PEER,
            notify_image=None,
            notify_title="New message",
            notify_content="Some one want to sent you a message",
            notify_platform="all"
        )
        new_group = self.model.add()
        # check queue and push
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            try:
                client_notify_queue[notify_channel].put(new_group)
            except Exception as e:
                logger.error(e)

    def notify_invite_group(self, client_id, ref_client_id, ref_group_id):
        self.model = Notify(
            client_id=client_id,
            ref_client_id=ref_client_id,
            ref_group_id=ref_group_id,
            notify_type=NEW_GROUP,
            notify_image=None,
            notify_title="Group Chat",
            notify_content="You are added to the group chat",
            notify_platform="all"
        )
        new_group = self.model.add()
        # check queue and push
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            try:
                client_notify_queue[notify_channel].put(new_group)
            except Exception as e:
                logger.error(e)

    def notify_client_update_peer_key(self, client_id, ref_client_id, ref_group_id):
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            try:
                notify = Notify(
                    id=0,
                    client_id=client_id,
                    ref_client_id=ref_client_id,
                    ref_group_id=ref_group_id,
                    notify_type=PEER_UPDATE_SIGNAL_KEY,
                    notify_image=None,
                    notify_title="",
                    notify_content="",
                    read_flg=False,
                    created_at=datetime.now()
                )
                client_notify_queue[notify_channel].put(notify)
            except Exception as e:
                logger.error(e)

    def notify_client_update_call(self, notify_type, client_id, ref_client_id, ref_group_id):
        notify_channel = "{}/notify".format(client_id)
        if notify_channel in client_notify_queue:
            try:
                notify = Notify(
                    id=0,
                    client_id=client_id,
                    ref_client_id=ref_client_id,
                    ref_group_id=ref_group_id,
                    notify_type=notify_type,
                    notify_image=None,
                    notify_title="",
                    notify_content="",
                    read_flg=False,
                    created_at=datetime.now()
                )
                client_notify_queue[notify_channel].put(notify)
                return True
            except Exception as e:
                logger.error(e)
                return False
        else:
            return False


