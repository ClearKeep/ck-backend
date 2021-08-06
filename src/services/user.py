from src.services.base import BaseService
from src.models.user import User
from src.models.mfa import MfaSetting
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils
from protos import user_pb2
from utils.logger import *
from msg.message import Message
import datetime
from utils.config import get_system_config, get_owner_workspace_domain
from utils.otp import OTPServer
from client.client_user import ClientUser

client_records_list_in_memory = {}


class UserService(BaseService):
    def __init__(self):
        super().__init__(User())
        self.mfa_setting = MfaSetting()
        self.otp_server = OTPServer()
        # self.workspace_domain = get_system_domain()

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
            logger.error(e)
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
            logger.info(bytes(str(e), encoding='utf-8'))
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
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.CHANGE_PASSWORD_FAILED)

    def init_mfa_state_changing(self, request_enable, user_id):
        user_info = self.model.get(user_id)
        user_mfa_setting = self.mfa_setting.get(user_id)
        # in case user_info is created but not user_info
        if user_mfa_setting is None and user_info is not None:
            self.mfa_setting = MfaSetting(
                id = user_id
            )
            self.mfa_setting.add()
            user_mfa_setting = self.mfa_setting.get(user_id)
        # when service start, we dont know number of remain_step so we set it to None
        if user_mfa_setting.mfa_enable == request_enable:
            # checking if mfa request state is the same with server
            remain_step = 0
        elif not request_enable:
            # in case disable mfa, we just turn off it directly without any additional checking
            user_mfa_setting.mfa_enable = request_enable
            user_mfa_setting.update()
            remain_step = 0
        else:
            # the final case when we enable mfa, we must verify phone_number here
            remain_step = 3
            if user_info.phone_number is None:
                raise Exception(Message.PHONE_NUMBER_NOT_FOUND)
            remain_step = 2
        return remain_step

    def init_otp(self, user_id):
        user_info = self.model.get(user_id)
        user_mfa_setting = self.mfa_setting.get(user_id)
        if user_mfa_setting.otp_frozen_time is not None and user_mfa_setting.otp_frozen_time > datetime.datetime.now():
            raise Exception(Message.NUMBER_OF_ATTEMPTS_OTP_EXCEEDED)
        otp = self.otp_server(user_info.phone_number)
        user_mfa_setting.otp = otp
        user_mfa_setting.otp_tried_times += 1
        user_mfa_setting.otp_created_time = datetime.datetime.now()
        user_mfa_setting.update()
        return otp

    def freeze_otp(self, user_id, frozen_time=600):
        user_mfa_setting = self.mfa_setting.get(user_id)
        user_mfa_setting.otp_tried_times = 0
        user_mfa_setting.otp = None
        # freeze otp service for 10 minutes
        user_mfa_setting.otp_frozen_time = datetime.datetime.now() + datetime.timedelta(seconds=frozen_time)
        return True

    def validate_password(self, user_id, password):
        user_info = self.model.get(user_id)
        try:
            token = KeyCloakUtils.token(user_info.email, password)
            logger.info(user_info.email, password)
            if token:
                self.init_otp(user_id)
                return True
            else:
                return False
                # raise Exception(Message.AUTH_USER_NOT_FOUND)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            return

    def validate_otp_and_enable_mfa(self, otp, user_id, valid_time=60, max_trying_times=5):
        valid_time = datetime.timedelta(seconds=valid_time)
        user_mfa_setting = self.mfa_setting.get(user_id)
        if otp == user_mfa_setting.otp and datetime.datetime.now() < user_mfa_setting.otp_created_time + valid_time:
            user_mfa_setting.mfa_enable = True
        elif user_mfa_setting.otp_tried_times < max_trying_times:
            self.init_otp(user_id)
        else:
            self.freeze_otp(user_id)
            raise Exception(Message.NUMBER_OF_ATTEMPTS_OTP_EXCEEDED)
        return user_mfa_setting.mfa_enable

    def change_mfa_state(self, request, state_keyword, user_id, remain_step=None):
        # we always start the mfa enable requesting with remain_step is None
        # remain_step must be handle only in server, client could only take it for knowing current state in
        # should re code to remove new_remain_step
        new_remain_step = 3
        if remain_step is None:
            # when service start, we dont know number of remain_step so we set it to None
            is_enable_request = state_keyword == "1"
            new_remain_step = self.init_mfa_state_changing(is_enable_request, user_id)
        elif remain_step == 2:
            # this remain_step specify that state_keyword must be the password of user
            if self.validate_password(user_id, state_keyword):
                new_remain_step = 1
            else:
                new_remain_step = 2
        elif remain_step == 1:
            if self.validate_otp_and_enable_mfa(state_keyword, user_id):
                new_remain_step = 0
            else:
                new_remain_step = 1
        else:
            # currently not taking any action for wrong passing remain_step
            new_remain_step = 0
        return new_remain_step

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
            logger.info(bytes(str(e), encoding='utf-8'))
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
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UPDATE_PROFILE_FAILED)

    def get_user_info(self, client_id, workspace_domain):
        try:
            user_info = self.model.get(client_id)
            if user_info is not None:
                return user_pb2.UserInfoResponse(
                    id=user_info.id,
                    display_name=user_info.display_name,
                    workspace_domain=workspace_domain
                )
            else:
                raise Exception(Message.GET_USER_INFO_FAILED)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
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
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.SEARCH_USER_FAILED)

    def get_users(self, client_id, workspace_domain):
        try:
            lst_user = self.model.get_users(client_id)
            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj.id,
                    display_name=obj.display_name,
                    workspace_domain=workspace_domain,
                )
                lst_obj_res.append(obj_res)

            response = user_pb2.GetUsersResponse(
                lst_user=lst_obj_res
            )
            return response
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_USER_INFO_FAILED)

    def update_last_login(self, user_id):
        try:
            user_info = self.model.get(user_id)
            user_info.last_login_at = datetime.datetime.now()
            user_info.update()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))

    def set_user_status(self, client_id, status):
        try:
            user_info = self.model.get(client_id)
            if status == "":
                status = None
            user_info.status = status

            user_info.update()
            client_record = client_records_list_in_memory.get(str(client_id), None)
            client_record["user_status"] = status
        except Exception as e:
            logger.error(e)
            raise Exception(Message.UPDATE_USER_STATUS_FAILED)

    def update_client_record(self, client_id):
        try:
            client_record = client_records_list_in_memory.get(str(client_id), None)
            if client_record is None:
                client_records_list_in_memory.update({
                    str(client_id): {
                        "last_active": datetime.datetime.now(),
                        "prev_active": None,
                        "user_status": None,
                    }
                })
            else:
                client_record["prev_active"] = client_record["last_active"]
                client_record["last_active"] = datetime.datetime.now()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.PING_PONG_SERVER_FAILED)

    def categorize_workspace_domains(self, list_clients):
        domain_local = get_owner_workspace_domain()
        workspace_domains_dictionary = {}

        for client in list_clients:
            if str(client.workspace_domain) in workspace_domains_dictionary:
                workspace_domains_dictionary[str(client.workspace_domain)].append(client)
            else:
                workspace_domains_dictionary.update({
                    str(client.workspace_domain): [client]
                })
        return workspace_domains_dictionary

    def get_list_clients_status(self, list_clients):
        logger.info("get_list_clients_status")
        try:
            owner_workspace_domain = get_owner_workspace_domain()
            list_clients_status = []

            workspace_domains_dictionary = self.categorize_workspace_domains(list_clients)

            for workspace_domain in workspace_domains_dictionary.keys():
                list_client = workspace_domains_dictionary[workspace_domain]
                if workspace_domain == owner_workspace_domain:
                    for client in list_client:
                        user_status = self.get_owner_workspace_client_status(client.client_id)

                        tmp_client_response = user_pb2.MemberInfoRes(
                            client_id=client.client_id,
                            workspace_domain=workspace_domain,
                            status=user_status,
                        )
                        list_clients_status.append(tmp_client_response)
                else:
                    other_clients_response = self.get_other_workspace_clients_status(workspace_domain, list_client)
                    list_clients_status.extend(other_clients_response)

            response = user_pb2.GetClientsStatusResponse(
                lst_client=list_clients_status
            )
            return response
        except Exception as e:
            logger.error(e)
            raise Exception(Message.GET_USER_STATUS_FAILED)

    def get_owner_workspace_client_status(self, client_id):
        logger.info("get_client_status")
        client_record = client_records_list_in_memory.get(str(client_id), None)

        if client_record is not None:
            leave_time_amount = datetime.datetime.now() - client_record["last_active"]

            if leave_time_amount.seconds > get_system_config().get("maximum_offline_time_limit"):
                user_status = "Offline"
            else:
                if client_record["user_status"] is not None:
                    user_status = client_record["user_status"]
                else:
                    user_status = "Active"
        else:
            user_status = "Undefined"
        return user_status

    def get_other_workspace_clients_status(self, workspace_domain, list_client):
        server_error_resp = []

        client = ClientUser(workspace_domain)
        client_resp = client.get_clients_status(list_client)

        if client_resp is None:
            logger.info("CALL WORKSPACE ERROR", workspace_domain)
            for client in list_client:
                tmp_client_response = user_pb2.MemberInfoRes(
                    client_id=client.client_id,
                    workspace_domain=client.workspace_domain,
                    status="Undefined",
                )
                server_error_resp.append(tmp_client_response)
            return server_error_resp
        return client_resp.lst_client
