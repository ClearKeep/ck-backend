from src.services.base import BaseService
from src.models.user import User
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils
from protos import user_pb2
from utils.config import get_system_domain, get_system_config
from utils.logger import *
from msg.message import Message
from utils.memory_storages import client_records_list_in_memory
from client.client_user import ClientUser
import datetime


class UserService(BaseService):
    def __init__(self):
        super().__init__(User())
        self.domain = get_system_domain()

    def create_new_user(self, id, email, display_name, auth_source):
        # password, first_name, last_name,
        try:
            self.model = User(
                id=id,
                email=email,
                display_name=display_name,
                auth_source=auth_source
            )
            # if email:
            #     self.model.email = EncryptUtils.encrypt_data(email, password, id)
            # if first_name:
            #     self.model.first_name = EncryptUtils.encrypt_data(first_name, password, id)
            # if last_name:
            #     self.model.last_name = EncryptUtils.encrypt_data(last_name, password, id)
            self.model.add()
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def create_user_social(self, id, email, display_name, auth_source):
        try:
            self.model = User(
                id=id,
                email=email,
                display_name=display_name,
                auth_source=auth_source,
                last_login_at=datetime.datetime.now()
            )
            # if email:
            #     self.model.email = EncryptUtils.encrypt_data(email, password, id)
            # if first_name:
            #     self.model.first_name = EncryptUtils.encrypt_data(first_name, password, id)
            # if last_name:
            #     self.model.last_name = EncryptUtils.encrypt_data(last_name, password, id)
            self.model.add()
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def get_google_user(self, email, auth_source):
        user_info = self.model.get_google_user(email, auth_source)
        return user_info

    def change_password(self, request, old_pass, new_pass, user_id):
        try:
            user_info = self.model.get(user_id)
            response = KeyCloakUtils.set_user_password(user_id, new_pass)
            # if user_info.email:
            #     email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
            #     user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
            # if user_info.first_name:
            #     first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
            #     user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
            # if user_info.last_name:
            #     last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)
            #     user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)

            return user_info.update()
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.CHANGE_PASSWORD_FAILED)

    def get_profile(self, user_id, hash_key):
        try:
            user_info = self.model.get(user_id)
            if user_info is not None:
                obj_res = user_pb2.UserProfileResponse(
                    id=user_info.id,
                    display_name=user_info.display_name
                )
                if user_info.email:
                    obj_res.email = user_info.email
                # if user_info.first_name:
                #     obj_res.first_name = EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key),
                # if user_info.last_name:
                #     obj_res.last_name = EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key),

                return obj_res
            else:
                return None
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_PROFILE_FAILED)

    def update_profile(self, request, user_id, hash_key):
        try:
            user_info = self.model.get(user_id)
            if request.display_name:
                user_info.display_name = request.display_name

            # if request.email:
            #     user_info.email = EncryptUtils.encrypt_with_hash(request.email, hash_key)
            # if request.first_name:
            #     user_info.first_name = EncryptUtils.encrypt_with_hash(request.first_name, hash_key)
            #
            # if request.last_name:
            #     user_info.last_name = EncryptUtils.encrypt_with_hash(request.last_name, hash_key)

            return user_info.update()
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UPDATE_PROFILE_FAILED)

    def get_user_info(self, client_id):
        try:
            user_info = self.model.get(client_id)
            if user_info is not None:
                return user_pb2.UserInfoResponse(
                    id=user_info.id,
                    display_name=user_info.display_name,
                    domain=self.domain
                )
            else:
                raise Exception(Message.GET_USER_INFO_FAILED)
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_USER_INFO_FAILED)

    def search_user(self, keyword, client_id):
        try:
            lst_user = self.model.search(keyword, client_id)
            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj.id,
                    display_name=obj.display_name,
                )
                lst_obj_res.append(obj_res)

            response = user_pb2.SearchUserResponse(
                lst_user=lst_obj_res
            )
            return response
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.SEARCH_USER_FAILED)

    def get_users(self, client_id):
        try:
            lst_user = self.model.get_users(client_id)
            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj.id,
                    display_name=obj.display_name,
                )
                lst_obj_res.append(obj_res)

            response = user_pb2.GetUsersResponse(
                lst_user=lst_obj_res
            )
            return response
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_USER_INFO_FAILED)

    def update_last_login(self, user_id):
        try:
            user_info = self.model.get(user_id)
            user_info.last_login_at = datetime.datetime.now()
            user_info.update()
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))


    def set_user_status(self, client_id, status):
        try:
            user_info = self.model.get(client_id)
            user_info.status = status
            user_info.update()
            client_record = client_records_list_in_memory.get(str(client_id), None)
            client_record["user_status"] = status
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UPDATE_USER_STATUS_FAILED)

    def update_client_record(self, client_id):
        print("update_client_record api - ping & pong server")
        try:
            client_record = client_records_list_in_memory.get(str(client_id), None)
            if client_record is None:
                client_records_list_in_memory.update({
                    str(client_id):{
                     "last_active" : datetime.datetime.now(),
                     "prev_active" : None,
                     "user_status" : None,
                        }
                    })
            else:
                client_record["prev_active"] = client_record["last_active"]
                client_record["last_active"] = datetime.datetime.now()
            print("client_record", client_records_list_in_memory)
        except Exception as e:
            logger.error(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.PING_PONG_SERVER_FAILED)

        
    def get_list_client_status(self, list_clients):
        print ("get_list_client_status")
        try:
            domain_local = get_system_domain()
            list_clients_status_res = []
            list_other_servers_clients = []
        
            for client in list_clients:
                if client.domain == domain_local:
                    user_status = self.get_client_status(client.client_id)
                    
                    if user_status is not None:
                        tmp_client_response = user_pb2.MemberInfoRes(
                                client_id=client.client_id,
                                domain=client.domain,
                                status=user_status,
                                )
                        list_clients_status_res.append(tmp_client_response)
                else:
                    list_other_servers_clients.append(client)
                    
            other_client_response = self.get_other_domains_client_status(list_other_servers_clients)
            
            if other_client_response is not None:
                list_clients_status_res.extend(other_client_response)
            response = user_pb2.GetClientsStatusResponse(
                    lst_client=list_clients_status_res
                )
            return response
        except Exception as e:
                logger.error(bytes(str(e), encoding='utf-8'))
                raise Exception(Message.GET_USER_STATUS_FAILED)
    
            
    def get_client_status(self, client_id):
        print("get_client_status api ")
    
        client_record = client_records_list_in_memory.get(str(client_id), None)
        
        if client_record is not None:
            leave_time_amount = datetime.datetime.now() - client_record["last_active"]
            
            if leave_time_amount.seconds > get_system_config().get("maximum_offline_time_limit"):
                client_record["user_status"] is None
                user_status = "Offline"
            else:
                if client_record["user_status"] is not None:
                    user_status = client_record["user_status"]
                else:
                    user_status = "Active"
        else:
            user_status = "Undefined"
            
        return user_status
        
    def get_other_domains_client_status(self, list_another_server_clients):
        if not list_another_server_clients:
            return None
        
        list_clients_status_res = []
        last_domain = None
        domain_list_client = []
        
        for client in list_another_server_clients:
            if client.domain == last_domain or last_domain == None:
                    domain_list_client.append(client)
            else:
                list_domain_client_status_res = self.get_response_from_domain(domain_list_client)
                list_clients_status_res.extend(list_domain_client_status_res)
            last_domain = client.domain
            
        list_domain_client_status_res = self.get_response_from_domain(domain_list_client)
        list_clients_status_res.extend(list_domain_client_status_res)
        
        return list_clients_status_res

                
    def get_response_from_domain(self,domain_list_client ):
        server_error_resp = []
        
        if domain_list_client:
            server_ip = domain_list_client[0].domain.split(':')[0]
            server_port = domain_list_client[0].domain.split(':')[1]
            client = ClientUser(server_ip,server_port)
            client_resp = client.get_client_status(domain_list_client)
            
            if client_resp is None:
                for client in domain_list_client:
                    tmp_client_response = user_pb2.MemberInfoRes(
                                client_id=client.client_id,
                                domain=client.domain,
                                status="Error",
                                )
                    server_error_resp.append(tmp_client_response)
                return server_error_resp
            return client_resp.lst_client
                
                