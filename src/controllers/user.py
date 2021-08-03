import protos.user_pb2 as user_messages
from src.controllers.base import *
from src.services.user import UserService
from middlewares.permission import *
from middlewares.request_logged import *
from utils.logger import *
from utils.config import get_system_domain, get_ip_domain
from client.client_user import *


class UserController(BaseController, user_pb2_grpc.UserServicer):
    def __init__(self, *kwargs):
        self.service = UserService()

    # @auth_required
    async def change_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            self.service.change_password(request, request.old_password, request.new_password, introspect_token['sub'])
            return user_messages.BaseResponse(success=True)

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    # @request_logged
    async def get_profile(self, request, context):
        print("user get_profile api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            user_info = self.service.get_profile(client_id, header_data['hash_key'])
            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_PROFILE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    async def update_profile(self, request, context):
        print("user update_profile api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            self.service.update_profile(request, client_id, header_data['hash_key'])
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_PROFILE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    # @request_logged
    async def get_user_info(self, request, context):
        try:
            client_id = request.client_id
            domain_client = request.domain
            domain_local = get_system_domain()
            if domain_local == domain_client:
                user_info = self.service.get_user_info(client_id)
            else:
                server_ip = get_ip_domain(domain_client)
                client = ClientUser(server_ip, get_system_config()['port'])
                user_info = client.get_user_info(client_id=client_id, domain=domain_client)
            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_USER_INFO_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def search_user(self, request, context):
        print("user search_user api")
        try:
            keyword = request.keyword
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            obj_res = self.service.search_user(keyword, client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_users(self, request, context):
        print("user get_users api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            obj_res = self.service.get_users(client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_user_domain(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            domain = "server.domain2"
            obj_res = self.service.get_users_domain(domain=domain)
            return obj_res
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # update status for user ("Active, Busy, Away, Do not disturb")
    @request_logged
    async def update_status(self, request, context):
        print("user update_status api")
        try:
            status = request.status
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            
            self.service.set_user_status(client_id, status)
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.UPDATE_USER_STATUS_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
    
    
    @request_logged
    async def ping_request(self, request, context):
        print("ping_pong_server api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            
            self.service.update_client_record(client_id)
            return user_messages.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.PING_PONG_SERVER_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            
            
    @request_logged
    async def get_client_status(self, request, context):
        print("get_client_status api")
        try:
            list_clients = request.lst_client
            list_clients.sort( key = lambda x:x.domain)
            list_user_status = self.service.get_list_client_status(list_clients)
            return list_user_status
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_USER_STATUS_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            
           
            
            
  
            
