from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.group import GroupService
from utils.config import get_owner_workspace_domain
from protos import group_pb2
from src.models.group import GroupChat
from client.client_group import *
from utils.keycloak import KeyCloakUtils
from google.protobuf.json_format import MessageToDict
import datetime


class GroupController(BaseController):
    def __init__(self, *kwargs):
        self.service = GroupService()

    @request_logged
    async def create_group(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # created_by_client_id = introspect_token['sub']
            group_name = request.group_name
            group_type = request.group_type
            lst_client = request.lst_client
            obj_res = self.service.add_group(group_name, group_type, lst_client, request.created_by_client_id)

            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
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
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_group(self, request, context):
        try:
            group_id = request.group_id
            # group = GroupChat().get_group(group_id)
            # if not group.owner_workspace_domain:
            obj_res = self.service.get_group(group_id)
            # else:
            #     get_group_request = group_pb2.GetGroupRequest(
            #         group_id=group.owner_group_id
            #     )
            #     obj_res = ClientGroup(
            #         group.owner_workspace_domain
            #     ).get_group(get_group_request)
            #     obj_res.group_id = group_id
            if obj_res is not None:
                return obj_res
            else:
                errors = [Message.get_error_object(Message.GROUP_CHAT_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_GROUP_CHAT_FAILED)]
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
            errors = [Message.get_error_object(Message.SEARCH_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_joined_groups(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # client_id = introspect_token['sub']
            obj_res = self.service.get_joined_group(request.client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def join_group(self, request, context):
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def remove_member(self, request, context):
        try:
            removed_member_info =\
                MessageToDict(
                    message=request.removed_member_info,
                    preserving_proto_field_name=True
                )
            removing_member_info =\
                MessageToDict(
                    message=request.removing_member_info,
                    preserving_proto_field_name=True
                )
            group = GroupService().get_group_info(request.group_id)
            current_group_clients = json.loads(group.group_clients)
            workspace_domains = list(set(
                [e['workspace_domain'] for e in current_group_clients
                 if ('status' not in e or
                     ('status' in e and e['status'] in ['active']))]
            ))
            logger.info(current_group_clients)
            logger.info(removed_member_info)
            logger.info(removing_member_info)
            for e in current_group_clients:
                logger.info(e)
                if ((e['id'] in [removed_member_info['id'],
                                 removing_member_info['id']]) and
                        ('status' in e and e['status'] in ['removed', 'left'])):
                    logger.info('Not in group 1')
                    raise Exception(Message.USER_NOT_IN_GROUP)
            if all([e['id'] != removed_member_info['id']
                    for e in current_group_clients]):
                logger.info('Not in group 2')
                raise Exception(Message.USER_NOT_IN_GROUP)
            else:
                group_clients_after_removal = []
                for e in current_group_clients:
                    if e['id'] == removed_member_info['id']:
                        if (removed_member_info['id'] ==
                                removing_member_info['id']):
                            e['status'] = 'left'
                        else:
                            e['status'] = 'removed'
                    group_clients_after_removal.append(e)

            if (group.owner_workspace_domain and
                    group.owner_workspace_domain !=
                    removing_member_info['workspace_domain']):
                res_obj = await self.service.remove_member_from_group_not_owner(
                    removed_member_info,
                    removing_member_info,
                    group,
                    group_clients_after_removal,
                    workspace_domains
                )
                return res_obj
            else:
                res_obj = await self.service.remove_member_from_group_owner(
                    removed_member_info,
                    removing_member_info,
                    group,
                    group_clients_after_removal,
                    workspace_domains
                )
                return res_obj
        except Exception as e:
            logger.error(e)
            errors = [
                e,
                Message.get_error_object(Message.REMOVE_MEMBER_FAILED)
            ]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def remove_member_workspace(self, request, context):
        try:
            groups = GroupChat().get_by_group_owner(request.owner_group_id)
            response = await self.service.remove_member_workspace(
                from_workspace_domain=request.from_workspace_domain,
                owner_workspace_domain=request.owner_workspace_domain,
                removed_member_info=MessageToDict(
                    request.removed_member_info,
                    preserving_proto_field_name=True
                ),
                removing_member_info=MessageToDict(
                    request.removing_member_info,
                    preserving_proto_field_name=True
                ),
                group=groups[0],  # arbitrary auxiliary group
                group_clients_after_removal=[
                    MessageToDict(e,
                                  preserving_proto_field_name=True)
                    for e in request.group_clients_after_removal
                ]
            )
            return response
        except Exception as e:
            logger.error(e)
            errors = [
                e,
                Message.get_error_object(Message.REMOVE_MEMBER_FAILED)
            ]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def leave_group(self, request, context):
        try:
            request = group_pb2.RemoveMemberRequest(
                removed_member_info=request.member_info,
                removing_member_info=request.member_info,
                group_id=request.group_id
            )
            response = await self.remove_member(request, context)
            return response
        except Exception as e:
            logger.error(e)
            errors = [
                e,
                Message.get_error_object(Message.LEAVE_GROUP_FAILED)
            ]
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
                        raise Exception(Message.ADDED_USER_IS_MEMBER)
                    if e['id'] == adding_member_info.id:
                        adding_member_in_group = True
            if not adding_member_in_group:
                raise Exception(Message.USER_NOT_IN_GROUP)

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
            #member_group.total_member = len(active_clients) + 1
            group.updated_by = adding_member_info.id
            group.updated_at = datetime.datetime.now()
            group.update()

            owner_workspace_domain = get_owner_workspace_domain()

            if (group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain):
                response = await self.service.add_member_to_group_not_owner(
                    added_member_info,
                    adding_member_info,
                    group,
                )
                return response
            else:
                response = await self.service.add_member_to_group_owner(
                    added_member_info,
                    adding_member_info,
                    group
                )
                return response
        except Exception as e:
            logger.error(e)
            errors = [
                e,
                Message.get_error_object(Message.ADD_MEMBER_FAILED)
            ]
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
            errors = [
                e,
                Message.get_error_object(Message.ADD_MEMBER_FAILED)
            ]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
