from src.services.base import BaseService
from src.models.group import GroupChat
from src.models.user import User
from src.models.message_user_read import MessageUserRead
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
import asyncio
from utils.config import *
from protos import group_pb2
from msg.message import Message
from google.protobuf.json_format import MessageToDict
from utils.logger import *
from src.services.notify_push import NotifyPushService
import logging
logger = logging.getLogger(__name__)

class GroupService(BaseService):
    """
    GroupService, involved in requests about creating new group, getting group information, or adding user to group/removing user from group
    """
    def __init__(self):
        super().__init__(GroupChat())
        self.notify_service = NotifyInAppService()
        self.transaction = 'ckbackendtransaction'

    def add_group(self, group_name, group_type, lst_client, created_by):
        # service for create new group with following info:
        # group_name: name of group in request, using for searching group
        # group_type: type of group in request, must be one of this values: [peer/group]
        # lst_client: list of client in this group
        # create_by: user_id of creator
        tmp_list_client = []
        created_by_user = None
        for obj in lst_client:
            if obj.id == created_by:
                created_by_user = obj
            tmp_list_client.append(
                {"id": obj.id, "display_name": obj.display_name, "workspace_domain": obj.workspace_domain,
                 "status": "active"})

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
                client_group_key = GroupClientKey().set_key(new_group.id, obj.id)
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

                group_res_object = \
                    ClientGroup(obj.workspace_domain).create_group_workspace(
                        request
                    )
                client_group_key = GroupClientKey().set_key(
                    new_group.id, obj.id,
                    group_res_object.client_workspace_domain,
                    group_res_object.group_id)
                client_group_key.add()
        return res_obj

    def add_group_workspace(self, group_name, group_type, from_client_id, client_id, lst_client, owner_group_id,
                            owner_workspace_domain):
        # workspace call for create a mapping group with reference info (owner_group_id, owner_workspace_domain) to origin group
        self.model = GroupChat(
            group_name=group_name,
            group_type=group_type,
            group_clients=lst_client,
            owner_group_id=owner_group_id,
            owner_workspace_domain=owner_workspace_domain,
            created_by=from_client_id,
            updated_at=datetime.datetime.now()
        )
        new_group = self.model.add()
        # add to signal group key
        client_group_key = GroupClientKey().set_key(new_group.id, client_id)
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
            self.notify_service.notify_invite_peer(client_id, from_client_id, new_group.id, owner_workspace_domain,
                                                   created_by_user['display_name'])
        else:
            self.notify_service.notify_invite_group(client_id, from_client_id, new_group.id, owner_workspace_domain,
                                                    created_by_user['display_name'])

        client_workspace_domain = get_owner_workspace_domain()
        return group_pb2.CreateGroupWorkspaceResponse(
            group_id=new_group.id,
            client_id=client_id,
            client_name=client_name,
            client_workspace_domain=client_workspace_domain
        )

    def register_webrtc_token(self, token):
        # register a webrtc_token
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
            logger.debug(json_response)
            raise Exception('Fail register webrtc token')

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
        # get basic group info stored in database by its group_id
        return self.model.get(group_id).GroupChat

    def get_group_info(self, group_id):
        # get group info for group id
        return self.model.get_group(group_id)

    def get_group(self, group_id, client_id):
        # get infor of client related to group stored in database by its group_id and client_id
        stored_client_key = GroupClientKey().get(group_id, client_id)
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

            if stored_client_key is not None:
                res_obj.client_key.workspace_domain = get_owner_workspace_domain()
                res_obj.client_key.clientId = stored_client_key.client_id
                if stored_client_key.device_id is not None:
                    res_obj.client_key.deviceId = stored_client_key.device_id
                if stored_client_key.client_key is not None:
                    res_obj.client_key.clientKeyDistribution = stored_client_key.client_key
                if stored_client_key.client_sender_key_id is not None:
                    res_obj.client_key.senderKeyId = stored_client_key.client_sender_key_id
                if stored_client_key.client_sender_key is not None:
                    res_obj.client_key.senderKey = stored_client_key.client_sender_key
                if stored_client_key.client_public_key is not None:
                    res_obj.client_key.publicKey = stored_client_key.client_public_key
                if stored_client_key.client_private_key is not None:
                    res_obj.client_key.privateKey = stored_client_key.client_private_key

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
        # searching groups with keyword return for related group_name, return satifying groups
        lst_group = self.model.search(keyword)
        lst_obj_res = []
        group_ids = (group.GroupChat.id for group in lst_group)

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
        # get all groups that this client has joined
        lst_group = self.model.get_joined(client_id)
        lst_obj_res = []
        group_ids = (group.GroupChat.id for group in lst_group)
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

            #client signal key of group
            group_client_key = item.GroupClientKey
            if group_client_key.client_id:
                obj_res.client_key.clientId = group_client_key.client_id
            if group_client_key.device_id:
                obj_res.client_key.deviceId = group_client_key.device_id

            if group_client_key.client_key:
                obj_res.client_key.clientKeyDistribution = group_client_key.client_key
            if group_client_key.client_sender_key_id:
                obj_res.client_key.senderKeyId = group_client_key.client_sender_key_id
            if group_client_key.client_sender_key:
                obj_res.client_key.senderKey = group_client_key.client_sender_key
            if group_client_key.client_public_key:
                obj_res.client_key.publicKey = group_client_key.client_public_key
            if group_client_key.client_private_key:
                obj_res.client_key.privateKey = group_client_key.client_private_key

            # check if this group has an unread message
            if obj.last_message_id:
                is_read = MessageUserRead().get_by_message_id(obj.last_message_id)
                if is_read:
                    obj_res.has_unread_message = False
                else:
                    obj_res.has_unread_message = True

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
                if obj_res.last_message.from_client_id == client_id:
                    obj_res.last_message.sender_message = last_message.sender_message
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

    async def forgot_peer_groups_for_client(self, user_info):
        # notify all other users involved in peer chat with that this user updated public key
        client_id = user_info.id
        lst_group = self.model.get_joined(client_id)
        owner_workspace_domain = get_owner_workspace_domain()
        informed_workspace_domain = {}
        logger.info("start forgot peer group for client {}".format(client_id))
        push_service = NotifyPushService()
        logger.info(lst_group)
        for group in lst_group:
            if group.GroupChat.group_type != "peer":
                continue
            logger.info("from group {}".format(group.GroupChat.id))
            lst_client = json.loads(group.GroupChat.group_clients)
            for client in lst_client:
                logger.info("notify to client {}".format(client["id"]))
                if client["id"] != client_id:
                    if client["workspace_domain"] == owner_workspace_domain:
                        try:
                            data = {
                                'client_id': client["id"],
                                'client_workspace_domain': owner_workspace_domain,
                                'group_id': str(group.GroupChat.id),
                                'deactive_account_id': client_id
                            }
                            await push_service.push_text_to_client(
                                to_client_id=client["id"],
                                title="Deactivate Member",
                                body="A user has been deactived",
                                from_client_id=client_id,
                                notify_type="deactive_account",
                                data=json.dumps(data)
                            )
                        except Exception as e:
                            logger.error("Cannot notify to client {}".format(client["id"]))
                            logger.error(e, exc_info=True)
                    else:
                        if client["workspace_domain"] not in informed_workspace_domain:
                            informed_workspace_domain[client["workspace_domain"]] = group_pb2.WorkspaceNotifyDeactiveMember(
                                                                                                          deactive_account_id=client_id
                                                                                                            )
                        informed_workspace_domain[client["workspace_domain"]].client_ids.append(client["id"])
        for workspace_domain in informed_workspace_domain:
            try:
                await ClientGroup(workspace_domain).workspace_notify_deactive_member(informed_workspace_domain[workspace_domain])
            except Exception as e:
                logger.error(e, exc_info=True)

    async def member_forgot_password_in_group(self, user_info):
        groups = self.model.get_joined_group_type(user_info.id, 'group')
        owner_workspace_domain = get_owner_workspace_domain()
        workspaces = set()
        for group in groups:
            clients = json.loads(group.GroupChat.group_clients)
            _clients = []
            for client in clients:
                if client['id'] != user_info.id:
                    _clients.append(client)
                if client["workspace_domain"] != owner_workspace_domain:
                    workspaces.add(client["workspace_domain"])

            group.GroupChat.group_clients = json.dumps(_clients)
            group.GroupChat.total_member = len(_clients)
            group.GroupChat.update()
        self.model.delete_group_client_key_by_client_id(user_info.id)

        await asyncio.gather(
            *[
                ClientGroup(workspace_domain).workspace_member_forgot_password_in_group(
                    group_pb2.WorkspaceMemberForgotPasswordInGroup(
                        user_id=user_info.id
                    )
                )
                for workspace_domain in workspaces
            ]
        )

    async def member_forgot_password_in_group(self, user_info):
        groups = self.model.get_joined_group_type(user_info.id, 'group')
        owner_workspace_domain = get_owner_workspace_domain()
        workspaces = set()
        for group in groups:
            clients = json.loads(group.GroupChat.group_clients)
            _clients = []
            for client in clients:
                if client['id'] != user_info.id:
                    _clients.append(client)
                if client["workspace_domain"] != owner_workspace_domain:
                    workspaces.add(client["workspace_domain"])

            group.GroupChat.group_clients = json.dumps(_clients)
            group.GroupChat.total_member = len(_clients)
            group.GroupChat.update()
        self.model.delete_group_client_key_by_client_id(user_info.id)

        await asyncio.gather(
            *[
                ClientGroup(workspace_domain).workspace_member_forgot_password_in_group(
                    group_pb2.WorkspaceMemberForgotPasswordInGroup(
                        user_id=user_info.id
                    )
                )
                for workspace_domain in workspaces
            ]
        )

    async def workspace_notify_deactive_member(self, deactive_account_id, client_ids):
        # workspace call for notify all other users in different server involved in peer chat with that this user updated public key
        push_service = NotifyPushService()
        for client_id in client_ids:
            try:
                user_info = User().get(client_id)
                if user_info is not None:
                    data = {
                            'client_id': client_id,
                            'deactive_account_id': deactive_account_id
                        }
                    await push_service.push_text_to_client(
                        to_client_id=client_id,
                        title="Deactivate Member",
                        body="A user has been deactived",
                        from_client_id=deactive_account_id,
                        notify_type="deactive_account",
                        data=json.dumps(data)
                    )
            except Exception as e:
                logger.error(e, exc_info=True)

    async def workspace_member_forgot_password_in_group(self, user_id):
        groups = self.model.get_joined_group_type(user_id, 'group')
        for group in groups:
            clients = json.loads(group.GroupChat.group_clients)
            clients = [
                client
                for client in clients
                if client['id'] != user_id
            ]
            group.GroupChat.group_clients = json.dumps(clients)
            group.GroupChat.total_member = len(clients)
            group.GroupChat.update()

        self.model.delete_group_client_key_by_client_id(user_id)

    async def workspace_member_forgot_password_in_group(self, user_id):
        groups = self.model.get_joined_group_type(user_id, 'group')
        for group in groups:
            clients = json.loads(group.GroupChat.group_clients)
            clients = [
                client
                for client in clients
                if client['id'] != user_id
            ]
            group.GroupChat.group_clients = json.dumps(clients)
            group.GroupChat.total_member = len(clients)
            group.GroupChat.update()

        self.model.delete_group_client_key_by_client_id(user_id)

    def get_clients_in_group(self, group_id):
        # get all client in group
        return GroupClientKey().get_clients_in_group(group_id)

    def get_clients_in_group_owner(self, group_owner_id):
        # get all client in groups
        lst_group = self.model.get_by_group_owner(group_owner_id)
        group_ids = (group.id for group in lst_group)
        return GroupClientKey().get_clients_in_groups(group_ids)

    async def add_member_to_group_not_owner(self, added_member_info, adding_member_info, group):
        # adding member to group not created in this server, with additional info about adding member and added member
        logger.info('add_member_to_group_not_owner')

        owner_workspace_domain = get_owner_workspace_domain()
        tmp_list_client = json.loads(group.group_clients)

        # PROCESS IN THIS SERVER
        # case new member is same server (not owner group)
        if added_member_info.workspace_domain == owner_workspace_domain:
            # add group with owner group
            self.model = GroupChat(
                owner_group_id=group.owner_group_id,
                owner_workspace_domain=group.owner_workspace_domain,
                group_name=group.group_name,
                group_type=group.group_type,
                group_clients=group.group_clients,
                group_rtc_token="",
                total_member=len(tmp_list_client),
                created_by=group.created_by,
            )
            new_group = self.model.add()
            added_member_info.ref_group_id = new_group.id

            # add more group client key
            group_client_key = GroupClientKey().set_key(
                new_group.id, added_member_info.id)
            group_client_key.add()

        # update all group with owner group
        lst_group = self.model.get_by_group_owner(group.owner_group_id)
        for group in lst_group:
            group.group_clients = group.group_clients
            group.total_member = len(tmp_list_client)
            group.update()

        # push notification for member active
        group_ids = (group.id for group in lst_group)
        list_clients = GroupClientKey().get_clients_in_groups(group_ids)
        push_service = NotifyPushService()

        for client in list_clients:
            data = {
                'client_id': client.GroupClientKey.client_id,
                'client_workspace_domain': owner_workspace_domain,
                'group_id': str(client.GroupClientKey.group_id),
                'added_member_id': added_member_info.id,
                'added_member_display_name': added_member_info.display_name,
                'added_member_workspace_domain': added_member_info.workspace_domain,
                'adding_member_id': adding_member_info.id,
                'adding_member_display_name': adding_member_info.display_name,
                'adding_member_workspace_domain': adding_member_info.workspace_domain
            }
            logger.info(data)
            # TODO: maybe handling push to owwner
            await push_service.push_text_to_client(
                to_client_id=client.GroupClientKey.client_id,
                title="Member Add",
                body="A user has been added to the group",
                from_client_id=adding_member_info.id,
                notify_type="new_member",
                data=json.dumps(data)
            )
        # END PROCESS IN THIS SERVER
        # CALL ADD MEMBER TO OWNER SERVER
        add_member_request = group_pb2.AddMemberRequest(
            added_member_info=added_member_info,
            adding_member_info=adding_member_info,
            group_id=group.owner_group_id,
        )
        ClientGroup(group.owner_workspace_domain).add_member(add_member_request)

        # for compatible with old code, should be remove in future?
        return group_pb2.BaseResponse()

    async def add_member_to_group_owner(self, added_member_info, adding_member_info, group):
        # adding member to group created in this server, with additional info about adding member and added member
        logger.info('add_member_to_group_owner')
        owner_workspace_domain = get_owner_workspace_domain()

        # add more group client key for group owner
        client_workspace_domain = None
        if added_member_info.workspace_domain != owner_workspace_domain:
            client_workspace_domain = added_member_info.workspace_domain

        group_client_key = GroupClientKey().set_key(
            group.id, added_member_info.id, client_workspace_domain, added_member_info.ref_group_id).add()

        # push notification for other member in server
        lst_client_in_group = self.get_clients_in_group(group.id)
        push_service = NotifyPushService()
        for client in lst_client_in_group:
            if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                if client.GroupClientKey.client_id != adding_member_info.id:
                    data = {
                        'client_id': client.GroupClientKey.client_id,
                        'client_workspace_domain': owner_workspace_domain,
                        'group_id': str(group.id),
                        'added_member_id': added_member_info.id,
                        'added_member_display_name': added_member_info.display_name,
                        'added_member_workspace_domain': owner_workspace_domain,
                        'adding_member_id': adding_member_info.id,
                        'adding_member_display_name': adding_member_info.display_name,
                        'adding_member_workspace_domain': owner_workspace_domain
                    }
                    logger.info(data)
                    # TODO: maybe handling push to owwner
                    await push_service.push_text_to_client(
                        to_client_id=client.GroupClientKey.client_id,
                        title="Member Add",
                        body="A user has been added to the group",
                        from_client_id=adding_member_info.id,
                        notify_type="new_member",
                        data=json.dumps(data)
                    )

        # request add member to other server
        informed_workspace_domain = []
        for client in lst_client_in_group:
            if client.GroupClientKey.client_workspace_domain and client.GroupClientKey.client_workspace_domain != owner_workspace_domain \
                    and client.GroupClientKey.client_workspace_domain != adding_member_info.workspace_domain:  # prevent loop call

                if client.GroupClientKey.client_workspace_domain in informed_workspace_domain:
                    continue
                informed_workspace_domain.append(client.GroupClientKey.client_workspace_domain)

                owner_group_req = group_pb2.GroupInfo(
                    group_id=group.id,
                    group_name=group.group_name,
                    group_type=group.group_type,
                    group_clients=group.group_clients,
                    group_workspace_domain=owner_workspace_domain,
                    created_by=group.created_by,
                )
                request = group_pb2.AddMemberWorkspaceRequest(
                    added_member_info=added_member_info,
                    adding_member_info=adding_member_info,
                    owner_group=owner_group_req
                )
                logger.info(
                    "call add member to workspace domain {}".format(client.GroupClientKey.client_workspace_domain))
                response = ClientGroup(client.GroupClientKey.client_workspace_domain).workspace_add_member(request)
                if response.is_member_workspace:
                    logger.info("update ref_group to main server {}".format(response.ref_group_id))
                    group_client_key.client_workspace_group_id = response.ref_group_id
                    group_client_key.update()

        # for compatible with old code, should be remove in future?
        return group_pb2.BaseResponse()

    async def workspace_add_member(self, added_member_info, adding_member_info, owner_group_info):
        # workspace adding member to group, with additional info about adding member, added member and original group
        logger.info('workspace_add_member')

        owner_workspace_domain = get_owner_workspace_domain()
        tmp_list_client = json.loads(owner_group_info.group_clients)

        is_member_workspace = False
        ref_group_id = None
        # create for new member
        if added_member_info.workspace_domain == owner_workspace_domain:
            is_member_workspace = True
            # add group with owner group
            self.model = GroupChat(
                owner_group_id=owner_group_info.group_id,
                owner_workspace_domain=owner_group_info.group_workspace_domain,
                group_name=owner_group_info.group_name,
                group_type=owner_group_info.group_type,
                group_clients=owner_group_info.group_clients,
                group_rtc_token="",
                total_member=len(tmp_list_client),
                created_by=owner_group_info.created_by,
            )
            new_group = self.model.add()
            ref_group_id = new_group.id
            # add more group client key
            group_client_key = GroupClientKey().set_key(
                new_group.id, added_member_info.id)
            group_client_key.add()

        # update all group with owner group
        lst_group = self.model.get_by_group_owner(owner_group_info.group_id)
        for group in lst_group:
            group.group_clients = owner_group_info.group_clients
            group.total_member = len(tmp_list_client)
            group.update()

        # push notification for member active
        group_ids = (group.id for group in lst_group)
        list_clients = GroupClientKey().get_clients_in_groups(group_ids)
        push_service = NotifyPushService()

        for client in list_clients:
            data = {
                'client_id': client.GroupClientKey.client_id,
                'client_workspace_domain': owner_workspace_domain,
                'group_id': str(client.GroupClientKey.group_id),
                'added_member_id': added_member_info.id,
                'added_member_display_name': added_member_info.display_name,
                'added_member_workspace_domain': added_member_info.workspace_domain,
                'adding_member_id': adding_member_info.id,
                'adding_member_display_name': adding_member_info.display_name,
                'adding_member_workspace_domain': adding_member_info.workspace_domain
            }
            logger.info(data)
            # TODO: maybe handling push to owwner
            await push_service.push_text_to_client(
                to_client_id=client.GroupClientKey.client_id,
                title="Member Add",
                body="A user has been added to the group",
                from_client_id=adding_member_info.id,
                notify_type="new_member",
                data=json.dumps(data)
            )

        return group_pb2.AddMemberWorkspaceResponse(
            is_member_workspace=is_member_workspace,
            ref_group_id=ref_group_id
        )

    async def leave_group_owner(self, leave_member, leave_member_by, group):
        # leave group service for group created in this server for user leave_member, called by leave_member_by
        logger.info('leave_group_owner')
        owner_workspace_domain = get_owner_workspace_domain()

        # delete group client key and inform member in this server
        push_service = NotifyPushService()
        lst_client_in_group = self.get_clients_in_group(group.id)

        # case group remain only one member
        if len(lst_client_in_group) == 1 and lst_client_in_group[0].GroupClientKey.client_id == leave_member.id:
            lst_client_in_group[0].GroupClientKey.delete()
            group.delete()
            return group_pb2.BaseResponse()

        for client in lst_client_in_group:
            if client.GroupClientKey.client_id == leave_member.id:
                client.GroupClientKey.delete()
            if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                if client.GroupClientKey.client_id != leave_member_by.id:
                    data = {
                        'client_id': client.GroupClientKey.client_id,
                        'client_workspace_domain': owner_workspace_domain,
                        'group_id': str(group.id),
                        'leave_member': leave_member.id,
                        'leave_member_display_name': leave_member.display_name,
                        'leave_member_workspace_domain': leave_member.workspace_domain,
                        'leave_member_by': leave_member_by.id,
                        'leave_member_by_display_name': leave_member_by.display_name,
                        'leave_member_by_workspace_domain': leave_member_by.workspace_domain
                    }
                    logger.info(data)
                    # TODO: maybe handling push to owwner
                    await push_service.push_text_to_client(
                        to_client_id=client.GroupClientKey.client_id,
                        title="Member leave",
                        body="user leave group",
                        from_client_id=leave_member_by.id,
                        notify_type="member_leave",
                        data=json.dumps(data)
                    )
        # call workspace leave for other server
        informed_workspace_domain = []
        for client in lst_client_in_group:
            if client.GroupClientKey.client_workspace_domain and client.GroupClientKey.client_workspace_domain != owner_workspace_domain \
                    and client.GroupClientKey.client_workspace_domain != leave_member_by.workspace_domain:  # prevent loop call

                if client.GroupClientKey.client_workspace_domain in informed_workspace_domain:
                    continue
                informed_workspace_domain.append(client.GroupClientKey.client_workspace_domain)

                owner_group_req = group_pb2.GroupInfo(
                    group_id=client.GroupClientKey.client_workspace_group_id,
                    group_name=group.group_name,
                    group_type=group.group_type,
                    group_clients=group.group_clients,
                    group_workspace_domain=owner_workspace_domain,
                    created_by=group.created_by,
                )
                request = group_pb2.WorkspaceLeaveGroupRequest(
                    leave_member=leave_member,
                    leave_member_by=leave_member_by,
                    owner_group=owner_group_req
                )
                logger.info(
                    "call leave member to workspace domain {}".format(client.GroupClientKey.client_workspace_domain))
                ClientGroup(client.GroupClientKey.client_workspace_domain).workspace_leave_group(request)

        # for compatible with old code, should be remove in future?
        return group_pb2.BaseResponse()

    async def leave_group_not_owner(self, leave_member, leave_member_by, group):
        # leave group service for group not created in this server for user leave_member, called by leave_member_by
        logger.info('leave_group_not_owner')
        owner_workspace_domain = get_owner_workspace_domain()
        tmp_list_client = json.loads(group.group_clients)
        # PROCESS IN THIS SERVER
        # case new member is same server (not owner group)
        if leave_member.workspace_domain == owner_workspace_domain:
            # remove group client add more group client key
            group_client_key = GroupClientKey().get(group.id, leave_member.id)
            if group_client_key:
                group_client_key.delete()
            # remove group with owner group
            group.delete()

        # update all group with owner group
        lst_group = self.model.get_by_group_owner(group.owner_group_id)
        for group in lst_group:
            group.group_clients = group.group_clients
            group.total_member = len(tmp_list_client)
            group.update()

        # push notification for member active
        group_ids = (group.id for group in lst_group)
        list_clients = GroupClientKey().get_clients_in_groups(group_ids)
        push_service = NotifyPushService()

        for client in list_clients:
            data = {
                'client_id': client.GroupClientKey.client_id,
                'client_workspace_domain': owner_workspace_domain,
                'group_id': str(group.id),
                'leave_member': leave_member.id,
                'leave_member_display_name': leave_member.display_name,
                'leave_member_workspace_domain': leave_member.workspace_domain,
                'leave_member_by': leave_member_by.id,
                'leave_member_by_display_name': leave_member_by.display_name,
                'leave_member_by_workspace_domain': leave_member_by.workspace_domain
            }
            logger.info(data)
            # TODO: maybe handling push to owner
            await push_service.push_text_to_client(
                to_client_id=client.GroupClientKey.client_id,
                title="Member leave",
                body="user leave group",
                from_client_id=leave_member_by.id,
                notify_type="member_leave",
                data=json.dumps(data)
            )
        # END PROCESS IN THIS SERVER
        # CALL LEAVE MEMBER TO OWNER SERVER
        leave_group_request = group_pb2.LeaveGroupRequest(
            leave_member=leave_member,
            leave_member_by=leave_member_by,
            group_id=group.owner_group_id,
        )
        ClientGroup(group.owner_workspace_domain).leave_group(leave_group_request)
        # for compatible with old code, should be remove in future?
        return group_pb2.BaseResponse()

    async def workspace_leave_group(self, leave_member, leave_member_by, group):
        # workspace called leave group, with additional info about leave_member, leave_member_by, group info
        logger.info('workspace_leave_group')

        owner_workspace_domain = get_owner_workspace_domain()
        tmp_list_client = json.loads(group.group_clients)

        owner_group_id = None
        group_this_workspace = self.get_group_info(group.group_id)
        if group_this_workspace:
            owner_group_id = group_this_workspace.owner_group_id

        # update all group with owner group
        if owner_group_id:
            lst_group = self.model.get_by_group_owner(owner_group_id)
            for gr in lst_group:
                gr.group_clients = group.group_clients
                gr.total_member = len(tmp_list_client)
                gr.update()

            # push notification for member active
            group_ids = (gr.id for gr in lst_group)
            list_clients = GroupClientKey().get_clients_in_groups(group_ids)
            push_service = NotifyPushService()

            for client in list_clients:
                data = {
                    'client_id': client.GroupClientKey.client_id,
                    'client_workspace_domain': owner_workspace_domain,
                    'group_id': str(client.GroupClientKey.group_id),
                    'leave_member': leave_member.id,
                    'leave_member_display_name': leave_member.display_name,
                    'leave_member_workspace_domain': leave_member.workspace_domain,
                    'leave_member_by': leave_member_by.id,
                    'leave_member_by_display_name': leave_member_by.display_name,
                    'leave_member_by_workspace_domain': leave_member_by.workspace_domain
                }
                logger.info(data)
                # TODO: maybe handling push to owwner
                await push_service.push_text_to_client(
                    to_client_id=client.GroupClientKey.client_id,
                    title="Member leave",
                    body="user leave group",
                    from_client_id=leave_member_by.id,
                    notify_type="member_leave",
                    data=json.dumps(data)
                )
                if leave_member.workspace_domain == owner_workspace_domain and leave_member.id == client.GroupClientKey.client_id:
                    client.GroupClientKey.delete()
                    #remove group
                    leave_member_group = self.get_group_info(client.GroupClientKey.group_id)
                    if leave_member_group:
                        leave_member_group.delete()

        # for compatible with old code, should be remove in future?
        return group_pb2.BaseResponse()
