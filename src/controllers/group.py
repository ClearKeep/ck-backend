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
            group = GroupChat().get_group(group_id)
            if not group.owner_workspace_domain:
                obj_res = self.service.get_group(group_id)
            else:
                get_group_request = group_pb2.GetGroupRequest(
                    group_id=group.owner_group_id
                )
                obj_res = ClientGroup(
                    group.owner_workspace_domain
                ).get_group(get_group_request)
                obj_res.group_id = group_id
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
    async def add_member(self, request, context):
        try:
            current_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(request.group_id)
            if (group.owner_workspace_domain and
                    group.owner_workspace_domain != current_workspace_domain):
                res_obj = self.service.add_member_to_group_not_owner(
                    request, group)
                return res_obj
            else:
                res_obj = self.service.add_member_to_group_owner(
                    request, group)
                return res_obj
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            return group_pb2.BaseResponse(
                success=False,
                errors=group_pb2.ErrorRes(
                    code=errors[0].code,
                    message=errors[0].message
                )
            )

    @request_logged
    async def add_member_workspace(self, request, context):
        try:
            obj_res = self.service.add_member_workspace(
                request.group_name,
                request.group_type,
                request.adding_member_id,
                request.adding_member_display_name,
                request.added_member_id,
                request.clients,
                request.owner_group_id,
                request.owner_workspace_domain,
                request.group_id,
                request.added_member_workspace_domain
            )
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.ADD_MEMBER_FAILED)]
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
            # metadata = dict(context.invocation_metadata())
            # access_token_information = KeyCloakUtils.introspect_token(
            #     metadata['access_token']
            # )
            # removing_member_info = {
            #     'id': access_token_information['sub'],
            #     'workspace_domain': get_owner_workspace_domain()
            # }
            removing_member_info =\
                MessageToDict(
                    message=request.removing_member_info,
                    preserving_proto_field_name=True
                )
            group = GroupService().get_group_info(request.group_id)
            current_group_clients = json.loads(group.group_clients)
            if all([e['id'] != removed_member_info['id']
                    for e in current_group_clients]):
                raise Exception(Message.USER_NOT_IN_GROUP)
            else:
                # group_clients_after_removal =\
                #     [e for e in current_group_clients
                #      if e['id'] != removed_member_info['id']]
                # assert len(group_clients_after_removal) == len(
                #     current_group_clients
                # ) - 1
                group_clients_after_removal = []
                for e in current_group_clients:
                    if e['id'] == removed_member_info['id']:
                        if (removed_member_info['id'] ==
                                removing_member_info['id']):
                            e['status'] = 'left'
                        else:
                            e['status'] = 'removed'
                    group_clients_after_removal.append(e)

            workspace_domains = list(set(
                [e['workspace_domain'] for e in current_group_clients]
            ))
            if (group.owner_workspace_domain and
                    group.owner_workspace_domain !=
                    removing_member_info['workspace_domain']):
                res_obj = self.service.remove_member_from_group_not_owner(
                    removed_member_info,
                    removing_member_info,
                    group,
                    group_clients_after_removal,
                    workspace_domains
                )
                return res_obj
            else:
                res_obj = self.service.remove_member_from_group_owner(
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
            response = self.service.remove_member_workspace(
                from_workspace_domain=request.from_workspace_domain,
                owner_workspace_domain=request.owner_workspace_domain,
                removed_member_info=MessageToDict(request.removed_member_info),
                removing_member_info=MessageToDict(
                    request.removing_member_info
                ),
                group=groups[0],  # arbitrary auxiliary group
                group_clients_after_removal=[
                    MessageToDict(e)
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
            metadata = dict(context.invocation_metadata())
            access_token_information = KeyCloakUtils.introspect_token(
                metadata['access_token']
            )
            removed_member_info = {
                'id': access_token_information['sub'],
                'workspace_domain': get_owner_workspace_domain()
            }
            request = group_pb2.RemoveMemberRequest(
                removed_member_info=self.service.dict_to_message(
                    removed_member_info),
                group_id=request.group_id
            )
            response = self.remove_member(request, context)
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
