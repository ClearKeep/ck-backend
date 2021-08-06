from src.services.base import BaseService
from src.models.user import User
from src.models.authen_setting import AuthenSetting
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
        self.authen_setting = AuthenSetting()
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

    def init_mfa_state_enabling(self, user_id):
        user_info = self.model.get(user_id)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            self.authen_setting = AuthenSetting(id=user_id)
            self.authen_setting.add()
            user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.mfa_enable:
            next_step = ''
        elif user_info.phone_number is None:
            raise Exception(Message.PHONE_NUMBER_NOT_FOUND)
        else:
            user_authen_setting.otp_changing_state = 1
            user_authen_setting.update()
            next_step = 'mfa_validate_password'
        return next_step

    def init_mfa_state_disabling(self, user_id):
        user_info = self.model.get(user_id)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            self.authen_setting = AuthenSetting(id=user_id)
            self.authen_setting.add()
            user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.mfa_enable:
            user_authen_setting.mfa_enable = False
            user_authen_setting.update()
        next_step = ''
        return next_step

    def init_otp_and_update(self, user_id, valid_time=60):
        user_info = self.model.get(user_id)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.otp_frozen_time is not None and user_authen_setting.otp_frozen_time > datetime.datetime.now():
            raise Exception(Message.NUMBER_OF_ATTEMPTS_OTP_EXCEEDED)
        otp = self.otp_server(user_info.phone_number)
        user_authen_setting.otp = otp
        user_authen_setting.otp_trying_times += 1
        user_authen_setting.otp_valid_time = datetime.datetime.now() + datetime.timedelta(seconds=valid_time)
        user_authen_setting.update()
        return otp

    def reset_otp_and_update(self, user_id):
        user_authen_setting = self.authen_setting.get(user_id)
        user_authen_setting.otp_trying_times = 0
        user_authen_setting.otp = None
        user_authen_setting.update()

    def freeze_otp_and_update(self, user_id, frozen_time=600):
        user_authen_setting = self.authen_setting.get(user_id)
        # freeze otp service for 10 minutes
        user_authen_setting.otp_frozen_time = datetime.datetime.now() + datetime.timedelta(seconds=frozen_time)
        self.reset_otp_and_update(user_id)
        return True

    def validate_password(self, user_id, password):
        user_info = self.model.get(user_id)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.otp_changing_state != 1:
            raise Exception(Message.AUTHEN_SETTING_FLOW_NOT_FOUND)
        try:
            token = KeyCloakUtils.token(user_info.email, password)
            logger.info(user_info.email, password)
            if token:
                user_authen_setting.otp_changing_state = 2
                user_authen_setting.update()
                self.init_otp_and_update(user_id)
                next_step = 'mfa_validate_otp'
            else:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            return next_step
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def validate_otp(self, user_id, otp, valid_time=60, max_trying_times=5):
        valid_time = datetime.timedelta(seconds=valid_time)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.otp_changing_state != 2:
            raise Exception(Message.AUTHEN_SETTING_FLOW_NOT_FOUND)
        if otp == user_authen_setting.otp and datetime.datetime.now() < user_authen_setting.otp_valid_time:
            user_authen_setting.mfa_enable = True
            user_authen_setting.otp_changing_state = 0
            user_authen_setting.update()
            self.reset_otp_and_update(user_id)
            next_step = ''
        elif user_authen_setting.otp_trying_times < max_trying_times:
            self.init_otp_and_update(user_id)
            next_step = 'mfa_validate_otp'
        else:
            next_step = ''
            user_authen_setting.otp_changing_state = 0
            self.freeze_otp_and_update(user_id)
            raise Exception(Message.NUMBER_OF_ATTEMPTS_OTP_EXCEEDED)
        return next_step

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
