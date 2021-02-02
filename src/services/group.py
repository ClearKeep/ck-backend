from src.services.base import BaseService
from src.models.group import GroupChat
from protos import group_pb2
from src.models.signal_group_key import GroupClientKey
from src.services.notify_inapp import NotifyInAppService
from src.services.janus_webrtc import JanusService
from utils.config import get_system_config
import requests
import json


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupChat())
        self.notify_service = NotifyInAppService()
        self.transaction = 'ckbackendtransaction'

    def add_group(self, group_name, group_type, lst_client_id, created_by):
        self.model = GroupChat(
            group_name=group_name,
            group_type=group_type,
            created_by=created_by
        )
        new_group = self.model.add()
        new_token = self.register_webrtc_token(new_group.group_rtc_token)
        self.create_rtc_group(new_group.id,new_token)
        res_obj = group_pb2.GroupObjectResponse(
            group_id=new_group.id,
            group_name=new_group.group_name,
            group_type=new_group.group_type,
            group_avatar=new_group.group_avatar,
            created_by_client_id=new_group.created_by,
            created_at=int(new_group.created_at.timestamp() * 1000),
            updated_by_client_id=new_group.updated_by,
            group_rtc_token=new_group.group_rtc_token

        )
        if new_group.updated_at is not None:
            res_obj.updated_at = int(new_group.updated_at.timestamp() * 1000)

        for obj in lst_client_id:
            # add to signal group key
            client_group_key = GroupClientKey().set_key(new_group.id, obj, None, None)
            client_group_key.add()
            # notify per client
            if group_type == "peer":
                self.notify_service.notify_invite_peer(obj, created_by, new_group.id)
            else:
                self.notify_service.notify_invite_group(obj, created_by, new_group.id)

        # list client in group
        lst_client_in_group = GroupClientKey().get_clients_in_group(new_group.id)
        for client in lst_client_in_group:
            client_in = group_pb2.ClientInGroupResponse(
                id=client.User.id,
                display_name=client.User.display_name
            )
            res_obj.lst_client.append(client_in)

        return res_obj

    def register_webrtc_token(self, token):
        payload = {
            "janus": 'add_token',
            "token": token,
            "transaction": self.transaction,
            "admin_secret": get_system_config()['janus_webrtc'].get('admin_secret')
        }
        rtc_admin_url = get_system_config()['janus_webrtc'].get('admin_url')
        # register token
        response = requests.post(rtc_admin_url, data=json.dumps(payload))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            return token
        else:
            raise

    def create_rtc_group(self, group_id, rtc_token):
        # create Janus
        janus = JanusService(janus_url=get_system_config()['janus_webrtc'].get('client_url'),
                             token=rtc_token,
                             stransaction=self.transaction)

        # create session
        response = requests.post(janus.janus_url, data=json.dumps(janus.get_janus_data(group_id=group_id)))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            janus.janus_sesion = json_response.get("data").get('id')
        else:
            raise

        # attach plugin
        janus.set_janus_plugin_url(janus.janus_sesion)
        response = requests.post(janus.janus_plugin_url, data=json.dumps(janus.get_janus_data_plugin()))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            janus.janus_plugin = json_response.get("data").get('id')
        else:
            raise

        # create room
        janus.set_janus_create_room_url(janus.janus_plugin)
        response = requests.post(janus.janus_create_room_url, data=json.dumps(janus.get_janus_create_room(group_id)))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            janus.janus_room = json_response.get("plugindata").get('data').get('room')
        else:
            raise

        return janus.janus_room

    def get_group(self, group_id):
        group = self.model.get(group_id)
        if group is not None:
            obj = group.GroupChat
            res_obj = group_pb2.GroupObjectResponse(
                group_id=obj.id,
                group_name=obj.group_name,
                group_type=obj.group_type,
                group_avatar=obj.group_avatar,
                created_by_client_id=obj.created_by,
                created_at=int(obj.created_at.timestamp() * 1000),
                updated_by_client_id=obj.updated_by,
                group_rtc_token=obj.group_rtc_token
            )
            if obj.updated_at is not None:
                res_obj.updated_at = int(obj.updated_at.timestamp() * 1000)

            # list client in group
            lst_client_in_group = GroupClientKey().get_clients_in_group(group_id)
            for client in lst_client_in_group:
                client_in = group_pb2.ClientInGroupResponse(
                    id=client.id,
                    display_name=client.display_name
                )
                res_obj.lst_client.append(client_in)

            if obj.last_message_at:
                res_obj.last_message_at = int(obj.last_message_at.timestamp() * 1000)

            # get last message
            if group.Message:
                last_message = group.Message
                res_obj.last_message.id = last_message.id
                res_obj.last_message.group_id = last_message.group_id
                res_obj.last_message.from_client_id = last_message.from_client_id
                res_obj.last_message.message = last_message.message
                res_obj.last_message.created_at = int(last_message.created_at.timestamp() * 1000)

                if last_message.client_id:
                    res_obj.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    res_obj.last_message.updated_at = int(last_message.updated_at.timestamp() * 1000)
                if last_message.client_id:
                    res_obj.last_message.group_type = "peer"
                else:
                    res_obj.last_message.group_type = "group"

            return res_obj
        else:
            return None

    def search_group(self, keyword):
        lst_group = self.model.search(keyword)
        lst_obj_res = []
        group_ids = (group.GroupChat.id for group in lst_group)
        lst_client_in_groups = GroupClientKey().get_clients_in_groups(group_ids)

        for item in lst_group:
            obj = item.GroupChat
            obj_res = group_pb2.GroupObjectResponse(
                group_id=obj.id,
                group_name=obj.group_name,
                group_type=obj.group_type,
                group_avatar=obj.group_avatar,
                created_by_client_id=obj.created_by,
                created_at=int(obj.created_at.timestamp() * 1000),
                updated_by_client_id=obj.updated_by,
                group_rtc_token = obj.group_rtc_token
            )
            if obj.updated_at is not None:
                obj_res.updated_at = int(obj.updated_at.timestamp() * 1000)

            if obj.last_message_at:
                obj_res.last_message_at = int(obj.last_message_at.timestamp() * 1000)

            for client in lst_client_in_groups:
                if client.group_id == obj.id:
                    client_in = group_pb2.ClientInGroupResponse(
                        id=client.User.id,
                        display_name=client.User.display_name
                    )
                    obj_res.lst_client.append(client_in)

            # get last message
            if item.Message:
                last_message = item.Message
                obj_res.last_message.id = last_message.id
                obj_res.last_message.group_id = last_message.group_id
                obj_res.last_message.from_client_id = last_message.from_client_id
                obj_res.last_message.message = last_message.message
                obj_res.last_message.created_at = int(last_message.created_at.timestamp() * 1000)

                if last_message.client_id:
                    obj_res.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    obj_res.last_message.updated_at = int(last_message.updated_at.timestamp() * 1000)
                if last_message.client_id:
                    obj_res.last_message.group_type = "peer"
                else:
                    obj_res.last_message.group_type = "group"

            lst_obj_res.append(obj_res)

        response = group_pb2.SearchGroupsResponse(
            lst_group=lst_obj_res
        )
        return response

    def get_joined_group(self, client_id):
        lst_group = self.model.get_joined(client_id)
        lst_obj_res = []
        group_ids = (group.GroupChat.id for group in lst_group)
        lst_client_in_groups = GroupClientKey().get_clients_in_groups(group_ids)

        for item in lst_group:
            obj = item.GroupChat
            obj_res = group_pb2.GroupObjectResponse(
                group_id=obj.id,
                group_type=obj.group_type,
                created_by_client_id=obj.created_by,
                created_at=int(obj.created_at.timestamp() * 1000),
                updated_by_client_id=obj.updated_by,
                group_rtc_token = obj.group_rtc_token
            )
            if obj.group_name:
                obj_res.group_name = obj.group_name

            if obj.group_avatar:
                obj_res.group_avatar = obj.group_avatar

            if obj.updated_at:
                obj_res.updated_at = int(obj.updated_at.timestamp() * 1000)

            for client in lst_client_in_groups:
                if client.group_id == obj.id:
                    client_in = group_pb2.ClientInGroupResponse(
                        id=client.User.id,
                        display_name=client.User.display_name
                    )
                    obj_res.lst_client.append(client_in)

            if obj.last_message_at:
                obj_res.last_message_at = int(obj.last_message_at.timestamp() * 1000)

            # get last message
            if item.Message:
                last_message = item.Message
                obj_res.last_message.id = last_message.id
                obj_res.last_message.group_id = last_message.group_id
                obj_res.last_message.from_client_id = last_message.from_client_id
                obj_res.last_message.message = last_message.message
                obj_res.last_message.created_at = int(last_message.created_at.timestamp() * 1000)

                if last_message.client_id:
                    obj_res.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    obj_res.last_message.updated_at = int(last_message.updated_at.timestamp() * 1000)
                if last_message.client_id:
                    obj_res.last_message.group_type = "peer"
                else:
                    obj_res.last_message.group_type = "group"

            lst_obj_res.append(obj_res)

        response = group_pb2.GetJoinedGroupsResponse(
            lst_group=lst_obj_res
        )
        return response

