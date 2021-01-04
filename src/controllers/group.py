from protos import group_pb2
from src.controllers.base import *
from src.services.signal import SignalService, client_queue
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.group import GroupService
from utils.config import get_system_domain, get_ip_domain
from client.client_group import *

class GroupController(BaseController):
    def __init__(self, *kwargs):
        self.service = GroupService()

    @request_logged
    def create_group(self, request, context):
        try:
            # header_data = dict(context.invocation_metadata())
            # introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            # created_by_client_id = introspect_token['sub']
            group_name = request.group_name
            group_type = request.group_type
            lst_client = list(request.lst_client)
            list_domain = set()
            list_domain_client = {}
            domain_local = get_system_domain()
            for client in lst_client:
                if client.client_domain in list_domain:
                    list_domain_client[str(client.client_domain)].append(client.client_id)
                else:
                    list_domain.add(str(client.client_domain))
                    list_domain_client[client.client_domain] = [client.client_id]

            def client_to_dict(domain,client_id):
                return {
                    'client_domain': domain,
                    'client_id': client_id
                }

            obj_res = []
            for client_domain,lst_client_id in list_domain_client.items():
                ref_group_id = request.ref_group_id
                ref_domain = request.ref_domain
                group_res = self.service.add_group(group_name, group_type, client_domain,
                                                 lst_client_id, request.created_by_client_id,
                                                 ref_group_id, ref_domain)
                ## check domain
                if client_domain != domain_local:
                    lst_client_to = [client_to_dict(domain=client_domain,client_id=client_id) for client_id in lst_client_id]
                    server_ip = get_ip_domain(client_domain)
                    client = ClientGroup(server_ip, get_system_config()['port'])
                    user_info = client.add_group(new_group=group_res,lst_client=lst_client_to,ref_domain=domain_local)

                obj_res.append(group_res)

            list_group_result = group_pb2.ListGroupObjectResponse(
                lst_group=obj_res
            )
            return list_group_result
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def get_group(self, request, context):
        try:
            group_id = request.group_id
            obj_res = self.service.get_group(group_id)
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
    def search_groups(self, request, context):
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
    def get_joined_groups(self, request, context):
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
    def invite_to_group(self, request, context):
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def join_group(self, request, context):
        try:
            pass
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
