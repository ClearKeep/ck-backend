from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.group import GroupService
from src.services.signal import SignalService
from utils.config import get_owner_workspace_domain
import protos.group_pb2 as group_messages
from src.models.group import GroupChat
from utils.keycloak import KeyCloakUtils
from google.protobuf.json_format import MessageToDict
import datetime


class GroupController(BaseController):
    def __init__(self, *kwargs):
        self.service = GroupService()

    @request_logged
    async def create_group(self, request, context):
        try:
            group_name = request.group_name
            group_type = request.group_type
            lst_client = request.lst_client
            obj_res = self.service.add_group(group_name, group_type, lst_client, request.created_by_client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def create_group_workspace(self, request, context):
        try:
            group_name = request.group_name
            group_type = request.group_type
            from_client_id = request.from_client_id
            client_id = request.client_id
            lst_client = request.lst_client
            owner_group_id = request.owner_group_id
            owner_workspace_domain = request.owner_workspace_domain
            obj_res = self.service.add_group_workspace(group_name, group_type, from_client_id, client_id, lst_client, owner_group_id,
                                                       owner_workspace_domain)

            return obj_res
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_group(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            group_id = request.group_id
            obj_res = self.service.get_group(group_id, client_id)

            if obj_res is not None:
                return obj_res
            else:
                raise Exception(Message.GROUP_CHAT_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_GROUP_CHAT_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def search_groups(self, request, context):
        try:
            keyword = request.keyword
            obj_res = self.service.search_group(keyword)
            return obj_res
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.SEARCH_GROUP_CHAT_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def get_joined_groups(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            obj_res = self.service.get_joined_group(client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def join_group(self, request, context):
        try:
            # TODO: implement this function
            pass
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)


    @request_logged
    async def add_member(self, request, context):
        try:
            group = GroupService().get_group_info(request.group_id)
            group_clients = json.loads(group.group_clients)
            added_member_info = request.added_member_info
            adding_member_info = request.adding_member_info

            #get workspace is active in group
            workspace_domains = list(set(
                [e['workspace_domain'] for e in group_clients
                 if ('status' not in e or
                     ('status' in e and e['status'] in ['active']))]
            ))
            logger.info(workspace_domains)

            #check added and adding member in group
            adding_member_in_group = False
            for e in group_clients:
                if 'status' not in e or e['status'] in ['active']:
                    if e['id'] == added_member_info.id:
                        raise Exception(Message.ADDED_USER_IS_ALREADY_MEMBER)
                    if e['id'] == adding_member_info.id:
                        adding_member_in_group = True
            if not adding_member_in_group:
                raise Exception(Message.ADDER_MEMBER_NOT_IN_GROUP)

            # new group clients
            new_group_clients = []
            is_old_member = False
            for e in group_clients:
                if e['id'] == added_member_info.id:
                    e['status'] = 'active'  # turn into active member
                    is_old_member = True
                new_group_clients.append(e)
            if not is_old_member:
                added_member_info.status = 'active'
                new_group_clients.append(
                    MessageToDict(
                        added_member_info,
                        preserving_proto_field_name=True
                    )
                )

            # update group members first
            group.group_clients = json.dumps(new_group_clients)
            group.updated_by = adding_member_info.id
            group.updated_at = datetime.datetime.now()
            group.update()

            owner_workspace_domain = get_owner_workspace_domain()

            # wait for service to add member to group, and return base response if no exception occured
            if (group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain):
                await self.service.add_member_to_group_not_owner(
                    added_member_info,
                    adding_member_info,
                    group,
                )
            else:
                await self.service.add_member_to_group_owner(
                    added_member_info,
                    adding_member_info,
                    group
                )

            return group_messages.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_add_member(self, request, context):
        try:
            added_member_info = request.added_member_info
            adding_member_info = request.adding_member_info
            owner_group = request.owner_group

            response = await self.service.workspace_add_member(
                added_member_info,
                adding_member_info,
                owner_group
            )
            return response
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def leave_group(self, request, context):
        try:
            leave_member = request.leave_member
            leave_member_by = request.leave_member_by

            new_member_status = "removed"
            if leave_member.id == leave_member_by.id:
                new_member_status = "leaved"

            group = GroupService().get_group_info(request.group_id)
            group_clients = json.loads(group.group_clients)

            leave_member_in_group = False
            leave_member_by_in_group = False
            for e in group_clients:
                if e['id'] == leave_member.id:
                    leave_member_in_group = True
                    e['status'] = new_member_status
                if e['id'] == leave_member_by.id:
                    leave_member_by_in_group = True
            if not leave_member_in_group:
                raise Exception(Message.LEAVED_MEMBER_NOT_IN_GROUP)
            if not leave_member_by_in_group and new_member_status == "removed":
                raise Exception(Message.REMOVER_MEMBER_NOT_IN_GROUP)

            # update field group_clients first
            logger.info("New group client: {}".format(group_clients))
            group.group_clients = json.dumps(group_clients)
            group.updated_by = leave_member_by.id
            group.update()

            owner_workspace_domain = get_owner_workspace_domain()

            # wait for service to leave group, and return base response if no exception occured
            if (group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain):
                await self.service.leave_group_not_owner(
                    leave_member,
                    leave_member_by,
                    group,
                )
            else:
                await self.service.leave_group_owner(
                    leave_member,
                    leave_member_by,
                    group,
                )

            return group_messages.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.LEAVE_GROUP_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_leave_group(self, request, context):
        try:
            leave_member = request.leave_member
            leave_member_by = request.leave_member_by
            owner_group = request.owner_group

            # wait for service to call workspace leave group, and return base response if no exception occured
            await self.service.workspace_leave_group(
                leave_member,
                leave_member_by,
                owner_group
            )
            return group_messages.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_notify_deactive_member(self, request, context):
        try:
            await self.service.workspace_notify_deactive_member(
                request.deactive_account_id,
                request.client_ids
            )
            return group_messages.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.LEAVE_GROUP_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
