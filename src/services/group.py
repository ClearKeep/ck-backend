from src.services.base import BaseService
from src.models.group import GroupChat
from proto import group_pb2
from src.models.signal_group_key import GroupClientKey
from src.services.notify import NotifyService


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupChat())
        self.notify_service = NotifyService()

    def add_group(self, group_name, group_type, lst_client_id, created_by):
        self.model = GroupChat(
            group_name=group_name,
            group_type=group_type,
            created_by=created_by
        )
        new_group = self.model.add()
        res_obj = group_pb2.GroupObjectResponse(
            group_id=new_group.id,
            group_name=new_group.group_name,
            group_type=new_group.group_type,
            group_avatar=new_group.group_avatar,
            created_by_client_id=new_group.created_by,
            created_at=int(new_group.created_at.timestamp()),
            updated_by_client_id=new_group.updated_by
        )
        if new_group.updated_at is not None:
            res_obj.updated_at = int(new_group.updated_at.timestamp())

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
        lst_client_in_group = GroupClientKey().get_all_in_group(new_group.id)

        for client in lst_client_in_group:
            res_obj.lst_client_id.append(client.client_id)

        return res_obj

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
                created_at=int(obj.created_at.timestamp()),
                updated_by_client_id=obj.updated_by
            )
            if obj.updated_at is not None:
                res_obj.updated_at = int(obj.updated_at.timestamp())

            # list client in group
            lst_client_in_group = GroupClientKey().get_all_in_group(group_id)
            for client in lst_client_in_group:
                res_obj.lst_client_id.append(client.client_id)

            if obj.last_message_at:
                res_obj.last_message_at = int(obj.last_message_at.timestamp())

            # get last message
            if group.Message:
                last_message = group.Message
                res_obj.last_message.id = last_message.id
                res_obj.last_message.group_id = last_message.group_id
                res_obj.last_message.from_client_id = last_message.from_client_id
                res_obj.last_message.message = last_message.message
                res_obj.last_message.created_at = int(last_message.created_at.timestamp())

                if last_message.client_id:
                    res_obj.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    res_obj.last_message.updated_at = int(last_message.updated_at.timestamp())
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
        for item in lst_group:
            obj = item.GroupChat
            obj_res = group_pb2.GroupObjectResponse(
                group_id=obj.id,
                group_name=obj.group_name,
                group_type=obj.group_type,
                group_avatar=obj.group_avatar,
                created_by_client_id=obj.created_by,
                created_at=int(obj.created_at.timestamp()),
                updated_by_client_id=obj.updated_by
            )
            if obj.updated_at is not None:
                obj_res.updated_at = int(obj.updated_at.timestamp())

            if obj.last_message_at:
                obj_res.last_message_at = int(obj.last_message_at.timestamp())

            # get last message
            if item.Message:
                last_message = item.Message
                obj_res.last_message.id = last_message.id
                obj_res.last_message.group_id = last_message.group_id
                obj_res.last_message.from_client_id = last_message.from_client_id
                obj_res.last_message.message = last_message.message
                obj_res.last_message.created_at = int(last_message.created_at.timestamp())

                if last_message.client_id:
                    obj_res.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    obj_res.last_message.updated_at = int(last_message.updated_at.timestamp())
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
                created_at=int(obj.created_at.timestamp()),
                updated_by_client_id=obj.updated_by
            )
            if obj.group_name:
                obj_res.group_name = obj.group_name

            if obj.group_avatar:
                obj_res.group_avatar = obj.group_avatar

            if obj.updated_at:
                obj_res.updated_at = int(obj.updated_at.timestamp())

            for client in lst_client_in_groups:
                if client.group_id == obj.id :
                    obj_res.lst_client_id.append(client.client_id)

            if obj.last_message_at:
                obj_res.last_message_at = int(obj.last_message_at.timestamp())

            # get last message
            if item.Message:
                last_message = item.Message
                obj_res.last_message.id = last_message.id
                obj_res.last_message.group_id = last_message.group_id
                obj_res.last_message.from_client_id = last_message.from_client_id
                obj_res.last_message.message = last_message.message
                obj_res.last_message.created_at = int(last_message.created_at.timestamp())

                if last_message.client_id:
                    obj_res.last_message.client_id = last_message.client_id
                if last_message.updated_at:
                    obj_res.last_message.updated_at = int(last_message.updated_at.timestamp())
                if last_message.client_id:
                    obj_res.last_message.group_type = "peer"
                else:
                    obj_res.last_message.group_type = "group"

            lst_obj_res.append(obj_res)

        response = group_pb2.GetJoinedGroupsResponse(
            lst_group=lst_obj_res
        )
        return response

