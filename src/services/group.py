from src.services.base import BaseService
from src.models.group import GroupChat
from src.models.user import User
from src.models.signal_group_key import GroupClientKey
from src.services.notify_inapp import NotifyInAppService
from src.services.janus_webrtc import JanusService
from client.client_group import *
from client.client_user import *
import requests
import secrets
import datetime
from utils.config import *
from protos import group_pb2
from msg.message import Message
from google.protobuf.json_format import MessageToDict


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupChat())
        self.notify_service = NotifyInAppService()
        self.transaction = 'ckbackendtransaction'

    def add_group(self, group_name, group_type, lst_client, created_by):
        # check duplicate with create group peer
        # if group_type == 'peer':
        #     group_chat = self.check_joined(create_by=created_by, list_client=lst_client)
        #     if group_chat:
        #         res_obj = group_pb2.GroupObjectResponse(
        #             group_id=group_chat.id,
        #             group_name=group_chat.group_name,
        #             group_type=group_chat.group_type,
        #             group_avatar=group_chat.group_avatar,
        #             created_by_client_id=group_chat.created_by,
        #             created_at=int(group_chat.created_at.timestamp() * 1000),
        #             updated_by_client_id=group_chat.updated_by,
        #             group_rtc_token=group_chat.group_rtc_token
        #         )
        #         return res_obj

        tmp_list_client = []
        created_by_user = None
        for obj in lst_client:
            if obj.id == created_by:
                created_by_user = obj
            tmp_list_client.append({"id": obj.id, "display_name": obj.display_name, "workspace_domain": obj.workspace_domain})

        self.model = GroupChat(
            group_name=group_name,
            group_type=group_type,
            group_clients=json.dumps(tmp_list_client),
            group_rtc_token=secrets.token_hex(10),
            total_member=len(tmp_list_client),
            created_by=created_by,
            updated_at=datetime.datetime.now()
        )
        new_group = self.model.add()

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

        owner_workspace_domain = get_owner_workspace_domain()
        for obj in lst_client:
            # list client in group
            client_in = group_pb2.ClientInGroupResponse(
                id=obj.id,
                display_name=obj.display_name,
                workspace_domain=obj.workspace_domain,
            )
            res_obj.lst_client.append(client_in)

            # add to signal group key
            if obj.workspace_domain == owner_workspace_domain:
                client_group_key = GroupClientKey().set_key(new_group.id, obj.id, None, None, None, None)
                client_group_key.add()
                # notify per client
                if group_type == "peer":
                    self.notify_service.notify_invite_peer(
                        obj.id,
                        created_by,
                        new_group.id,
                        created_by_user.workspace_domain,
                        created_by_user.display_name
                    )
                else:
                    self.notify_service.notify_invite_group(
                        obj.id,
                        created_by,
                        new_group.id,
                        created_by_user.workspace_domain,
                        created_by_user.display_name
                    )
            else:
                # need to call other workspace and create group key
                request = group_pb2.CreateGroupWorkspaceRequest(
                    group_name=group_name,
                    group_type=group_type,
                    from_client_id=created_by,
                    client_id=obj.id,
                    lst_client=new_group.group_clients,
                    owner_group_id=new_group.id,
                    owner_workspace_domain=owner_workspace_domain
                )

                group_res_object =\
                    ClientGroup(obj.workspace_domain).create_group_workspace(
                        request
                    )
                client_group_key = GroupClientKey().set_key(
                    new_group.id, obj.id,
                    group_res_object.client_workspace_domain,
                    group_res_object.group_id, None, None
                )
                client_group_key.add()
                # client_in = group_pb2.ClientInGroupResponse(
                #     id=group_res_object.client_id,
                #     display_name=group_res_object.client_name,
                #     workspace_domain=group_res_object.client_workspace_domain
                # )
                # res_obj.lst_client.append(client_in)

        # list client in group
        # lst_client_in_group = GroupClientKey().get_clients_in_group(new_group.id)
        # for client in lst_client_in_group:
        #     if client.GroupClientKey.client_workspace_domain is None:
        #         client_in = group_pb2.ClientInGroupResponse(
        #             id=client.User.id,
        #             display_name=client.User.display_name,
        #             workspace_domain=owner_workspace_domain
        #         )
        #         res_obj.lst_client.append(client_in)
        return res_obj

    def add_group_workspace(self, group_name, group_type, from_client_id, client_id, lst_client, owner_group_id, owner_workspace_domain):
        self.model = GroupChat(
            group_name=group_name,
            group_type=group_type,
            group_clients=lst_client,
            owner_group_id=owner_group_id,
            owner_workspace_domain=owner_workspace_domain,
            updated_at=datetime.datetime.now()
        )
        new_group = self.model.add()
        # add to signal group key
        client_group_key = GroupClientKey().set_key(new_group.id, client_id, None, None, None, None)
        client_group_key.add()

        client_name = ""
        user_info = User().get(client_id)
        if user_info:
            client_name = user_info.display_name

        list_client_in_group = json.loads(lst_client)
        created_by_user = None
        for obj in list_client_in_group:
            if obj['id'] == from_client_id:
                created_by_user = obj


        # notify to client
        if group_type == "peer":
            self.notify_service.notify_invite_peer(client_id, from_client_id, new_group.id, owner_workspace_domain, created_by_user['display_name'])
        else:
            self.notify_service.notify_invite_group(client_id,from_client_id, new_group.id, owner_workspace_domain, created_by_user['display_name'])

        client_workspace_domain = get_owner_workspace_domain()
        return group_pb2.CreateGroupWorkspaceResponse(
            group_id=new_group.id,
            client_id=client_id,
            client_name=client_name,
            client_workspace_domain=client_workspace_domain
        )

    def register_webrtc_token(self, token):
        self.token = token
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
            if json_response.get("janus") == 'error':
                janus.janus_sesion = json_response.get("session_id")
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

        # check room
        janus.set_janus_create_room_url(janus.janus_plugin)
        response = requests.post(janus.janus_create_room_url, data=json.dumps(janus.check_janus_create_room(group_id)))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            if json_response.get("plugindata").get('data').get('error_code') == 427:
                return group_id

        # create room
        response = requests.post(janus.janus_create_room_url, data=json.dumps(janus.get_janus_create_room(group_id)))
        json_response = json.loads(response.text)
        if json_response.get("janus") == 'success':
            janus.janus_room = json_response.get("plugindata").get('data').get('room')
        else:
            raise

        return janus.janus_room

    def get_group_obj(self, group_id):
        return self.model.get(group_id).GroupChat

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
            group_clients = json.loads(obj.group_clients)
            for client in group_clients:
                client_in = group_pb2.ClientInGroupResponse(
                    id=client['id'],
                    display_name=client['display_name'],
                    workspace_domain=client['workspace_domain'],
                )
                res_obj.lst_client.append(client_in)
            # lst_client_in_group = GroupClientKey().get_clients_in_group(group_id)
            # owner_workspace_domain = get_owner_workspace_domain()
            #
            # for client in lst_client_in_group:
            #     if client.GroupClientKey.client_workspace_domain is None:
            #         client_in = group_pb2.ClientInGroupResponse(
            #             id=client.User.id,
            #             display_name=client.User.display_name,
            #             workspace_domain=owner_workspace_domain,
            #         )
            #         res_obj.lst_client.append(client_in)
            #     else:
            #         #call to other workspace domain to get client
            #         client_in_workspace = ClientUser(client.GroupClientKey.client_workspace_domain).get_user_info(client.GroupClientKey.client_id, client.GroupClientKey.client_workspace_domain )
            #         client_in = group_pb2.ClientInGroupResponse(
            #             id=client_in_workspace.id,
            #             display_name=client_in_workspace.display_name,
            #             workspace_domain=client.GroupClientKey.client_workspace_domain
            #         )
            #         res_obj.lst_client.append(client_in)

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
                group_rtc_token=obj.group_rtc_token
            )
            if obj.updated_at is not None:
                obj_res.updated_at = int(obj.updated_at.timestamp() * 1000)

            if obj.last_message_at:
                obj_res.last_message_at = int(obj.last_message_at.timestamp() * 1000)

            # for client in lst_client_in_groups:
            #     if client.group_id == obj.id:
            #         client_in = group_pb2.ClientInGroupResponse(
            #             id=client.User.id,
            #             display_name=client.User.display_name
            #         )
            #         obj_res.lst_client.append(client_in)

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
                group_rtc_token=obj.group_rtc_token
            )
            if obj.group_name:
                obj_res.group_name = obj.group_name

            if obj.group_avatar:
                obj_res.group_avatar = obj.group_avatar

            if obj.updated_at:
                obj_res.updated_at = int(obj.updated_at.timestamp() * 1000)

            group_clients = json.loads(obj.group_clients)
            for client in group_clients:
                client_in = group_pb2.ClientInGroupResponse(
                    id=client['id'],
                    display_name=client['display_name'],
                    workspace_domain=client['workspace_domain'],
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

                for client_read_item in last_message.users_read:
                    client_read = group_pb2.ClientReadObject(
                        id=client_read_item.user.id,
                        display_name=client_read_item.user.display_name,
                        avatar=client_read_item.user.avatar
                    )
                    obj_res.last_message.lst_client_read.append(client_read)

            lst_obj_res.append(obj_res)

        response = group_pb2.GetJoinedGroupsResponse(
            lst_group=lst_obj_res
        )
        return response

    def check_joined(self, create_by, list_client):
        lst_group_peer = self.model.get_joined_group_type(client_id=create_by, group_type="peer")
        for member in list_client:
            member_id = member.id
            if member_id != create_by:
                for group_joined in lst_group_peer:
                    if group_joined.group_clients:
                        lst_group_client = json.loads(group_joined.group_clients)
                        lst_group_client_id = [item["id"] for item in lst_group_client]
                        if member_id in lst_group_client_id:
                            return group_joined.GroupChat
        return None

    def get_group_info(self, group_id):
        return self.model.get_group(group_id)

    def get_clients_in_group(self, group_id):
        return GroupClientKey().get_clients_in_group(group_id)

    def get_clients_in_group_owner(self, group_owner_id):
        lst_group = self.model.get_by_group_owner(group_owner_id)
        group_ids = (group.id for group in lst_group)
        return GroupClientKey().get_clients_in_groups(group_ids)

    def add_member_to_group_not_owner(self, request, group):
        """docstring for add_member_to_group_not_owner"""
        # client will handle the situation when group_type = 'peer'
        assert group.group_type == 'group'
        added_member_info = request.added_member_info
        current_group_clients = json.loads(group.group_clients)
        for client in current_group_clients:
            if added_member_info.id == client['id']:
                # this user is already a member of the group
                raise Exception(Message.ADD_MEMBER_FAILED)
            if request.adding_member_id == client['id']:
                adding_member_info = client
        current_group_clients.append(
            MessageToDict(
                message=added_member_info,
                preserving_proto_field_name=True
            )
        )
        for g in GroupChat().get_by_group_owner(group.owner_group_id):
            g.group_clients = json.dumps(current_group_clients)
            g.total_member = len(current_group_clients)
            g.updated_by = adding_member_info['id']
            g.updated_at = datetime.datetime.now()
            g.update()
        group = GroupChat().get_group(group.id)
        if (request.added_member_info.workspace_domain !=
                get_owner_workspace_domain()):
            request.group_id = group.owner_group_id
            add_member_res =\
                ClientGroup(
                    group.owner_workspace_domain  # 15000
                ).add_member(
                    request
                )
            return add_member_res
        else:
            # create a new record in group_chat table
            self.model = GroupChat(
                group_name=group.group_name,
                group_type=group.group_type,
                group_clients=group.group_clients,
                total_member=len(current_group_clients),
                owner_group_id=group.owner_group_id,
                owner_workspace_domain=group.owner_workspace_domain,
                updated_at=datetime.datetime.now(),
                updated_by=request.adding_member_id
            )
            new_group = self.model.add()
            # create a new record in group_client_key table
            group_client_key = GroupClientKey().set_key(
                new_group.id, added_member_info.id,
                None, None, None, None
            )
            group_client_key.add()
            # notification for the new client
            self.notify_service.notify_invite_group(
                added_member_info.id,
                adding_member_info['id'],
                new_group.id,
                group.owner_workspace_domain,  # ???
                adding_member_info['display_name']
            )
            add_member_workspace_request = group_pb2.AddMemberWorkspaceRequest(
                group_name=group.group_name,
                group_type=group.group_type,
                adding_member_id=adding_member_info['id'],
                adding_member_display_name=adding_member_info['display_name'],
                added_member_id=added_member_info.id,
                clients=group.group_clients,
                owner_group_id=group.owner_group_id,
                owner_workspace_domain=group.owner_workspace_domain,
                group_id=new_group.id,
                added_member_workspace_domain=request.added_member_info.workspace_domain
            )
            add_member_workspace_res =\
                ClientGroup(
                    group.owner_workspace_domain  # 15000
                ).add_member_workspace(
                    add_member_workspace_request
                )
            # group_client_key = GroupClientKey().set_key(
            #     group.id,
            #     added_member_info.id,
            #     added_member_info.workspace_domain,
            #     add_member_workspace_res.group_id, None, None
            # )
            # group_client_key.add()
            return group_pb2.BaseResponse(
                success=True
            )

    def add_member_to_group_owner(self, request, group):
        """docstring for add_member_to_group_owner"""
        # client will handle the situation when group_type = 'peer'
        assert group.group_type == 'group'
        added_member_info = request.added_member_info
        # update the existing record in group_chat table
        current_group_clients = json.loads(group.group_clients)
        for client in current_group_clients:
            if added_member_info.id == client['id']:
                # this user is already a member of the group
                raise Exception(Message.ADD_MEMBER_FAILED)
            if request.adding_member_id == client['id']:
                adding_member_info = client
        current_group_clients.append(
            MessageToDict(
                message=added_member_info,
                preserving_proto_field_name=True
            )
        )
        group.group_clients = json.dumps(current_group_clients)
        group.total_member = len(current_group_clients)
        group.updated_by = adding_member_info['id']
        group.updated_at = datetime.datetime.now()
        group.update()
        owner_workspace_domain = get_owner_workspace_domain()
        if (added_member_info.workspace_domain == owner_workspace_domain):
            # create a new record in group_client_key table
            group_client_key = GroupClientKey().set_key(
                group.id,
                added_member_info.id,
                None, None, None, None
            )
            group_client_key.add()
            # notification for the new client
            self.notify_service.notify_invite_group(
                added_member_info.id,
                adding_member_info['id'],
                group.id,
                owner_workspace_domain,
                adding_member_info['display_name']
            )
        add_member_workspace_request = group_pb2.AddMemberWorkspaceRequest(
            group_name=group.group_name,
            group_type=group.group_type,
            adding_member_id=adding_member_info['id'],
            adding_member_display_name=adding_member_info['display_name'],
            added_member_id=added_member_info.id,
            clients=group.group_clients,
            owner_group_id=group.id,
            owner_workspace_domain=owner_workspace_domain,
            group_id=None,
            added_member_workspace_domain=request.added_member_info.workspace_domain
        )
        group_workspaces = set([e['workspace_domain']
                                for e in current_group_clients])
        # group_workspaces = ['localhost:15000', 'localhost:25000']
        for ws in group_workspaces:
            if ws == owner_workspace_domain:
                continue
            if ws == adding_member_info['workspace_domain']:
                continue
            # if ws == 'localhost:15000':
            #     continue
            # if ws == 'localhost:25000':
            #     continue
            add_member_workspace_res =\
                ClientGroup(
                    ws  # added_member_info.workspace_domain, ws
                ).add_member_workspace(
                    add_member_workspace_request
                )
            if ws == added_member_info.workspace_domain:
                group_client_key = GroupClientKey().set_key(
                    group.id,
                    added_member_info.id,
                    added_member_info.workspace_domain,
                    add_member_workspace_res.group_id, None, None
                )
                group_client_key.add()
        return group_pb2.BaseResponse(
            success=True
        )

    def add_member_workspace(
            self,
            group_name,
            group_type,
            adding_member_id,
            adding_member_display_name,
            added_member_id,
            clients,
            owner_group_id,
            owner_workspace_domain,
            group_id,
            added_member_workspace_domain):
        clients = json.loads(clients)
        current_workspace_domain = get_owner_workspace_domain()
        if current_workspace_domain != owner_workspace_domain:
            # from Main server -> Sub server
            # create a new record in group_chat table
            for g in GroupChat().get_by_group_owner(owner_group_id):
                g.group_clients = json.dumps(clients)
                g.total_member = len(clients)
                g.updated_by = adding_member_id
                g.updated_at = datetime.datetime.now()
                g.update()
            self.model = GroupChat(
                group_name=group_name,
                group_type=group_type,
                group_clients=json.dumps(clients),
                total_member=len(clients),
                owner_group_id=owner_group_id,
                owner_workspace_domain=owner_workspace_domain,
                updated_at=datetime.datetime.now(),
                updated_by=adding_member_id
            )
            new_group = self.model.add()
            # create a new record in group_client_key table
            group_client_key = GroupClientKey().set_key(
                new_group.id, added_member_id,
                None, None, None, None
            )
            group_client_key.add()
            # notification for the new client
            self.notify_service.notify_invite_group(
                added_member_id,
                adding_member_id,
                new_group.id,
                owner_workspace_domain,
                adding_member_display_name
            )
            return group_pb2.AddMemberWorkspaceResponse(
                group_id=new_group.id,
            )
        else:
            # from Sub server -> Main server
            # update the existing record in group_chat table
            group = self.get_group_info(owner_group_id)
            group.group_clients = json.dumps(clients)
            group.total_member = len(clients)
            group.updated_by = adding_member_id
            group.updated_at = datetime.datetime.now()
            group.update()
            # create a new record in group_client_key table
            group_client_key = GroupClientKey().set_key(
                group.id, added_member_id,
                added_member_workspace_domain, group_id, None, None
            )
            group_client_key.add()
            return group_pb2.AddMemberWorkspaceResponse(
                group_id=group.id
            )
