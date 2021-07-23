from src.services.base import BaseService
from src.models.group import GroupChat
from src.models.user import User
from src.models.signal_group_key import GroupClientKey
from src.models.signal_peer_key import PeerClientKey
from src.models.message import Message as MessageClass
from src.services.notify_inapp import NotifyInAppService
import src.services.notify_inapp as notify_inapp
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
from utils.logger import *
from src.services.notify_push import NotifyPushService


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
            tmp_list_client.append({"id": obj.id, "display_name": obj.display_name, "workspace_domain": obj.workspace_domain, "status": "active"})

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
                status="active"
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
                    status=client['status']
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
                    status=client['status']
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

    def remove_member_from_group_not_owner(
            self,
            removed_member_info,
            removing_member_info,
            group,
            group_clients_after_removal,
            workspace_domains):
        """docstring for remove_member_from_group_not_owner"""
        logger.info('remove_member_from_group_not_owner')
        assert len(json.loads(group.group_clients)) > 1
        owner_workspace_domain = group.owner_workspace_domain
        current_workspace_domain = get_owner_workspace_domain()
        # update_this_server_first = (
        #     current_workspace_domain == removed_member_info['workspace_domain']
        # )
        # if update_this_server_first:
        #     remove_member_workspace(
        #         from_workspace_domain=current_workspace_domain,
        #         owner_workspace_domain=owner_workspace_domain,
        #         removed_member_info=removed_member_info,
        #         removing_member_info=removing_member_info,
        #         group=group,
        #         group_clients_after_removal=group_clients_after_removal
        #     )
        request = group_pb2.RemoveMemberRequest(
            removed_member_info=self.dict_to_message(removed_member_info),
            removing_member_info=self.dict_to_message(removing_member_info),
            group_id=group.owner_group_id
        )
        response =\
            ClientGroup(
                owner_workspace_domain
            ).remove_member(
                request
            )
        # update the information in this auxil server based on the response
        self.remove_member_workspace(
            from_workspace_domain=current_workspace_domain,
            owner_workspace_domain=owner_workspace_domain,
            removed_member_info=removed_member_info,
            removing_member_info=removing_member_info,
            group=group,
            group_clients_after_removal=group_clients_after_removal
        )
        response.group_id = group.id
        return response

    def remove_member_from_group_owner(
            self,
            removed_member_info,
            removing_member_info,
            group,
            group_clients_after_removal,
            workspace_domains):
        """docstring for remove_member_from_group_owner"""
        logger.info('remove_member_from_group_owner')
        assert len(json.loads(group.group_clients)) >= 1
        owner_workspace_domain = get_owner_workspace_domain()
        # update information in the server of the removed member first
        workspace_domains.remove(removed_member_info['workspace_domain'])
        workspace_domains.insert(0, removed_member_info['workspace_domain'])
        for workspace_domain in workspace_domains:
            if workspace_domain == owner_workspace_domain:
                continue
            elif workspace_domain == removing_member_info['workspace_domain']:
                continue
            request = group_pb2.RemoveMemberWorkspaceRequest(
                from_workspace_domain=get_owner_workspace_domain(),
                owner_workspace_domain=owner_workspace_domain,
                removed_member_info=self.dict_to_message(removed_member_info),
                removing_member_info=self.dict_to_message(removing_member_info),
                owner_group_id=group.id,
                group_clients_after_removal=[
                    self.dict_to_message(e) for e in group_clients_after_removal
                ]
            )
            response =\
                ClientGroup(
                    workspace_domain
                ).remove_member_workspace(
                    request
                )
            if workspace_domain == removed_member_info['workspace_domain']:
                # keep the response if it is from workspace domain of the
                # removed member
                kept_response = response
            else:
                # use kept response to update information in the main server
                # and the other remaining servers
                pass
        self.remove_member_workspace(
            from_workspace_domain=get_owner_workspace_domain(),
            owner_workspace_domain=owner_workspace_domain,
            removed_member_info=removed_member_info,
            removing_member_info=removing_member_info,
            group=group,
            group_clients_after_removal=group_clients_after_removal
        )
        last_message = None if group.last_message_id is None\
            else MessageClass().get(message_id=group.last_message_id)
        return group_pb2.GroupObjectResponse2(
            group_id=group.id,
            group_name=group.group_name,
            group_avatar=group.group_avatar,
            group_type=group.group_type,
            lst_client=[
                self.dict_to_message(e)
                for e in group_clients_after_removal
            ],
            last_message_at=None if group.last_message_at is None\
                else int(group.last_message_at.timestamp() * 1000),
            last_message=None if last_message is None\
            else group_pb2.MessageObjectResponse(
                id=last_message.id,
                group_id=last_message.group_id,
                group_type=group.group_type,
                from_client_id=last_message.from_client_id,
                client_id=last_message.client_id,
                message=last_message.message,
                created_at=None if last_message.created_at is None\
                    else int(last_message.created_at.timestamp() * 1000),
                updated_at=None if last_message.updated_at is None\
                    else int(last_message.updated_at.timestamp() * 1000),
            ),
            created_by_client_id=group.created_by,
            updated_by_client_id=group.updated_by,
            created_at=None if group.created_at is None\
                else int(group.created_at.timestamp() * 1000),
            updated_at=None if group.updated_at is None\
                else int(group.updated_at.timestamp() * 1000),
            group_rtc_token=group.group_rtc_token
        )

    def remove_member_workspace(
            self,
            from_workspace_domain,
            owner_workspace_domain,
            removed_member_info,
            removing_member_info,
            group,
            group_clients_after_removal):
        logger.info('remove_member_workspace')
        current_workspace_domain = get_owner_workspace_domain()
        current_group_clients = json.loads(group.group_clients)
        active_clients =\
            [e for e in current_group_clients
             if 'status' not in e or e['status'] in ['active']]
        is_owner = (current_workspace_domain == owner_workspace_domain)
        if is_owner:
            if group.group_type == 'group':
                get_client_key = GroupClientKey().get
            elif group.group_type == 'peer':
                get_client_key = PeerClientKey().get
            else:
                raise ValueError
        else:
            if group.group_type == 'group':
                get_client_key = GroupChat().get_client_key_by_owner_group
            elif group.group_type == 'peer':
                get_client_key = GroupChat().get_client_key_by_owner_peer
            else:
                raise ValueError
        for client in active_clients:
            if client['workspace_domain'] != current_workspace_domain:
                if not is_owner:
                    continue
                else:
                    if client['id'] != removed_member_info['id']:
                        continue
            client_key = get_client_key(
                group.id if is_owner else group.owner_group_id,
                client['id']
            )
            member_group = GroupChat().get_group(client_key.group_id)
            if (client['id'] == removed_member_info['id']):
                client_key.delete()
                removed_member_info['group'] = member_group
                if is_owner:
                    if len(active_clients) == 1:
                        member_group.delete()
                    elif len(active_clients) > 1:
                        member_group.group_clients =\
                            json.dumps(group_clients_after_removal)
                        member_group.total_member =\
                            len(active_clients) - 1
                        member_group.updated_by = removing_member_info['id']
                        member_group.updated_at = datetime.datetime.now()
                        member_group.update()
                    else:
                        raise ValueError
                else:
                    member_group.delete()
                    # member_group.group_clients =\
                    #     json.dumps(group_clients_after_removal)
                    # member_group.total_member = len(group_clients_after_removal)
                    # member_group.updated_by = removing_member_info['id']
                    # member_group.updated_at = datetime.datetime.now()
                    # member_group.update()
            elif not is_owner:
                member_group.group_clients =\
                    json.dumps(group_clients_after_removal)
                member_group.total_member = len(active_clients) - 1
                member_group.updated_by = removing_member_info['id']
                member_group.updated_at = datetime.datetime.now()
                member_group.update()
            try:
                logger('inapp notification: services')
                self.notify_service.notify_removing_member(
                    client['id'],
                    client['workspace_domain'],
                    removed_member_info['id'],
                    removed_member_info['workspace_domain'],
                    member_group.id,
                    removed_member_info['display_name'],
                    notify_inapp.MEMBER_REMOVAL\
                    if removed_member_info['id'] != removing_member_info['id']\
                    else notify_inapp.MEMBER_LEAVE
                )
            except Exception as e:
                logger.info('Inapp notification is not working now')
                push_service = NotifyPushService()
                data = {
                    'nclient_id': client['id'],
                    'nclient_workspace_domain': client['workspace_domain'],
                    'group_id': member_group.id,
                    'removed_member_id': removed_member_info['id'],
                    'removed_member_workspace_domain': removed_member_info['workspace_domain'],
                    'removing_member_id': removing_member_info['id'],
                    'removing_member_workspace_domain': removing_member_info['workspace_domain']
                }
                push_service.push_text_to_client(
                    removed_member_info['id'],
                    title="Member Removal (Leave)",
                    body="A user removed (left) to the group",
                    from_client_id=removed_member_info['id'],
                    notify_type="old_member",
                    data=json.dumps(data)
                )
        if from_workspace_domain == current_workspace_domain:
            # return results to current server
            return True
        else:
            # return gRPC response message to requesting server
            return group_pb2.BaseResponse(success=True)

    def add_member_to_group_not_owner(
            self,
            added_member_info,
            adding_member_info,
            group,
            new_state,
            workspace_domains):
        logger.info('add_member_to_group_not_owner')
        owner_workspace_domain = group.owner_workspace_domain
        current_workspace_domain = get_owner_workspace_domain()
        update_this_server_first = (
            current_workspace_domain == added_member_info.workspace_domain
        )
        if update_this_server_first:
            response = self.add_member_workspace(
                from_workspace_domain=current_workspace_domain,
                owner_workspace_domain=owner_workspace_domain,
                added_member_info=added_member_info,
                adding_member_info=adding_member_info,
                group=group,
                new_state=new_state
            )
        request = group_pb2.AddMemberWorkspaceRequest(
            from_workspace_domain=current_workspace_domain,
            owner_workspace_domain=owner_workspace_domain,
            added_member_info=added_member_info,
            adding_member_info=adding_member_info,
            group=group_pb2.GroupInfo(
                group_clients=[self.dict_to_message(e)
                               for e in json.loads(group.group_clients)],
                group_type=group.group_type,
                group_name=group.group_name,
                id=group.id if not update_this_server_first else\
                    response['auxil_group_id'],
                owner_group_id=group.owner_group_id,
                owner_workspace_domain=group.owner_workspace_domain
            ),
            resulting_group_clients=[
                self.dict_to_message(e)
                for e in new_state['resulting_group_clients']
            ]
        )
        response =\
            ClientGroup(
                owner_workspace_domain
            ).add_member_workspace(
                request
            )
        if not update_this_server_first:
            # update the information in this auxil server based on the response
            self.add_member_workspace(
                from_workspace_domain=current_workspace_domain,
                owner_workspace_domain=owner_workspace_domain,
                added_member_info=added_member_info,
                adding_member_info=adding_member_info,
                group=group,
                new_state=new_state
            )
        response.group_id = group.id
        return response

    def add_member_to_group_owner(
            self,
            added_member_info,
            adding_member_info,
            group,
            new_state,
            workspace_domains):
        logger.info('add_member_to_group_owner')
        owner_workspace_domain = get_owner_workspace_domain()
        update_this_server_first = (
            adding_member_info.workspace_domain ==\
            added_member_info.workspace_domain
        )
        if update_this_server_first:
            self.add_member_workspace(
                from_workspace_domain=get_owner_workspace_domain(),
                owner_workspace_domain=owner_workspace_domain,
                added_member_info=added_member_info,
                adding_member_info=adding_member_info,
                group=group,
                new_state=new_state
            )
        if added_member_info.workspace_domain in workspace_domains:
            workspace_domains.remove(added_member_info.workspace_domain)
        workspace_domains.insert(0, added_member_info.workspace_domain)
        # workspace_domains = ['localhost:15000', 'localhost:25000']
        for workspace_domain in workspace_domains:
            if workspace_domain == owner_workspace_domain:
                continue
            elif workspace_domain == adding_member_info.workspace_domain:
                continue
            # if workspace_domain == 'localhost:25000':
            #     continue
            # elif workspace_domain == 'localhost:25000':
            #     continue
            request = group_pb2.AddMemberWorkspaceRequest(
                from_workspace_domain=get_owner_workspace_domain(),
                owner_workspace_domain=owner_workspace_domain,
                added_member_info=added_member_info,
                adding_member_info=adding_member_info,
                group=group_pb2.GroupInfo(
                    group_clients=[self.dict_to_message(e)
                                   for e in json.loads(group.group_clients)],
                    group_type=group.group_type,
                    group_name=group.group_name,
                    id=None,
                    owner_group_id=group.id,
                    owner_workspace_domain=get_owner_workspace_domain()
                ),
                resulting_group_clients=[
                    self.dict_to_message(e)
                    for e in new_state['resulting_group_clients']
                ]
            )
            response =\
                ClientGroup(
                    workspace_domain
                ).add_member_workspace(
                    request
                )
            if workspace_domain == added_member_info.workspace_domain:
                # keep the response if it is from workspace domain of the
                # removed member
                new_state['auxil_group_id'] = response.group_id
            else:
                # use kept response to update information in the main server
                # and the other remaining servers
                pass
        if not update_this_server_first:
            self.add_member_workspace(
                from_workspace_domain=get_owner_workspace_domain(),
                owner_workspace_domain=owner_workspace_domain,
                added_member_info=added_member_info,
                adding_member_info=adding_member_info,
                group=group,
                new_state=new_state
            )
        last_message = None if group.last_message_id is None\
            else MessageClass().get(message_id=group.last_message_id)
        return group_pb2.GroupObjectResponse2(
            group_id=group.id,
            group_name=group.group_name,
            group_avatar=group.group_avatar,
            group_type=group.group_type,
            lst_client=[
                self.dict_to_message(e)
                for e in new_state['resulting_group_clients']
            ],
            last_message_at=None if group.last_message_at is None\
                else int(group.last_message_at.timestamp() * 1000),
            last_message=None if last_message is None\
            else group_pb2.MessageObjectResponse(
                id=last_message.id,
                group_id=last_message.group_id,
                group_type=group.group_type,
                from_client_id=last_message.from_client_id,
                client_id=last_message.client_id,
                message=last_message.message,
                created_at=None if last_message.created_at is None\
                    else int(last_message.created_at.timestamp() * 1000),
                updated_at=None if last_message.updated_at is None\
                    else int(last_message.updated_at.timestamp() * 1000),
            ),
            created_by_client_id=group.created_by,
            updated_by_client_id=group.updated_by,
            created_at=None if group.created_at is None\
                else int(group.created_at.timestamp() * 1000),
            updated_at=None if group.updated_at is None\
                else int(group.updated_at.timestamp() * 1000),
            group_rtc_token=group.group_rtc_token
        )

    def add_member_workspace(
            self,
            from_workspace_domain,
            owner_workspace_domain,
            added_member_info,
            adding_member_info,
            group,
            new_state):
        logger.info('add_member_workspace')
        current_workspace_domain = get_owner_workspace_domain()
        if isinstance(group, GroupChat):
            # database -> Python
            current_group_clients = json.loads(group.group_clients)
        else:
            # gRPC -> Python
            current_group_clients = [
                MessageToDict(e, preserving_proto_field_name=True)
                for e in group.group_clients
            ]
        active_clients =\
            [e for e in current_group_clients
             if 'status' not in e or e['status'] in ['active']]
        is_owner = (current_workspace_domain == owner_workspace_domain)
        if is_owner:
            if group.group_type == 'group':
                get_client_key = GroupClientKey().get
            elif group.group_type == 'peer':
                raise ValueError
                get_client_key = PeerClientKey().get
            else:
                raise ValueError
        else:
            if group.group_type == 'group':
                get_client_key = GroupChat().get_client_key_by_owner_group
            elif group.group_type == 'peer':
                raise ValueError
                get_client_key = GroupChat().get_client_key_by_owner_peer
            else:
                raise ValueError
        already_updated = False
        for client in active_clients:
            if client['workspace_domain'] != current_workspace_domain:
                continue
            if not already_updated:
                client_key = get_client_key(
                    group.id if is_owner else group.owner_group_id,
                    client['id']
                )
                member_group = GroupChat().get_group(client_key.group_id)
                member_group.group_clients =\
                    json.dumps(new_state['resulting_group_clients'])
                member_group.total_member = len(active_clients) + 1
                member_group.updated_by = adding_member_info.id
                member_group.updated_at = datetime.datetime.now()
                member_group.update()
                if is_owner:
                    already_updated = True
            try:
                self.notify_service.notify_adding_member(
                    client['id'],
                    client['workspace_domain'],
                    added_member_info.id,
                    added_member_info.workspace_domain,
                    member_group.id,
                    added_member_info.display_name,
                    notify_inapp.MEMBER_ADD
                )
            except Exception as e:
                logger.info('Inapp notification is not working now')
                push_service = NotifyPushService()
                data = {
                    'nclient_id': client['id'],
                    'nclient_workspace_domain': client['workspace_domain'],
                    'group_id': member_group.id,
                    'added_member_id': added_member_info.id,
                    'added_member_workspace_domain': added_member_info.workspace_domain,
                    'adding_member_id': adding_member_info.id,
                    'adding_member_workspace_domain': adding_member_info.workspace_domain
                }
                push_service.push_text_to_client(
                    client['id'],
                    title="Member Add",
                    body="A user has been added to the group",
                    from_client_id=added_member_info.id,
                    notify_type="new_member",
                    data=json.dumps(data)
                )
        new_group = None
        if is_owner:
            if added_member_info.workspace_domain == current_workspace_domain:
                group_client_key = GroupClientKey().set_key(
                    group.id, added_member_info.id,
                    None, None, None, None
                )
                group_client_key.add()
                # notify added member
                try:
                    self.notify_service.notify_adding_member(
                        added_member_info.id,
                        added_member_info.workspace_domain,
                        added_member_info.id,
                        added_member_info.workspace_domain,
                        member_group.id,
                        added_member_info.display_name,
                        notify_inapp.MEMBER_ADD
                    )
                except Exception as e:
                    logger.info('Inapp notification is not working now')
                    push_service = NotifyPushService()
                    data = {
                        'nclient_id': added_member_info.id,
                        'nclient_workspace_domain': added_member_info.workspace_domain,
                        'group_id': member_group.id,
                        'added_member_id': added_member_info.id,
                        'added_member_workspace_domain': added_member_info.workspace_domain,
                        'adding_member_id': adding_member_info.id,
                        'adding_member_workspace_domain': adding_member_info.workspace_domain
                    }
                    push_service.push_text_to_client(
                        added_member_info.id,
                        title="Member Add",
                        body="A user has been added to the group",
                        from_client_id=added_member_info.id,
                        notify_type="new_member",
                        data=json.dumps(data)
                    )
            else:
                group_client_key = GroupClientKey().set_key(
                    group.id, added_member_info.id,
                    added_member_info.workspace_domain,
                    new_state['auxil_group_id'],
                    None, None
                )
                group_client_key.add()
        elif added_member_info.workspace_domain == current_workspace_domain:
            self.model = GroupChat(
                group_name=group.group_name,
                group_type=group.group_type,
                group_clients=json.dumps(
                    new_state['resulting_group_clients']),
                total_member=len(active_clients) + 1,
                owner_group_id=group.owner_group_id,
                owner_workspace_domain=group.owner_workspace_domain,
                updated_at=datetime.datetime.now(),
                updated_by=adding_member_info.id
            )
            new_group = self.model.add()
            group_client_key = GroupClientKey().set_key(
                new_group.id, added_member_info.id,
                None, None, None, None
            )
            group_client_key.add()
            # notify added member
            try:
                self.notify_service.notify_adding_member(
                    added_member_info.id,
                    added_member_info.workspace_domain,
                    added_member_info.id,
                    added_member_info.workspace_domain,
                    new_group.id,
                    added_member_info.display_name,
                    notify_inapp.MEMBER_ADD
                )
            except Exception as e:
                logger.info('Inapp notification is not working now')
                push_service = NotifyPushService()
                data = {
                    'nclient_id': added_member_info.id,
                    'nclient_workspace_domain': added_member_info.workspace_domain,
                    'group_id': new_group.id,
                    'added_member_id': added_member_info.id,
                    'added_member_workspace_domain': added_member_info.workspace_domain,
                    'adding_member_id': adding_member_info.id,
                    'adding_member_workspace_domain': adding_member_info.workspace_domain
                }
                push_service.push_text_to_client(
                    added_member_info.id,
                    title="Member Add",
                    body="A user has been added to the group",
                    from_client_id=added_member_info.id,
                    notify_type="new_member",
                    data=json.dumps(data)
                )
            new_state['auxil_group_id'] = new_group.id
        if from_workspace_domain == current_workspace_domain:
            # return results to current server
            return new_state
        else:
            # return gRPC response message to requesting server
            return group_pb2.GroupObjectResponse2(
                group_id=member_group.id\
                    if new_group is None else new_group.id
            )

    def dict_to_message(self, d):
        m = group_pb2.MemberInfo(
            id=d['id'],
            display_name=d['display_name'],
            workspace_domain=d['workspace_domain'],
            status=None if 'status' not in d else d['status']
        )
        return m
