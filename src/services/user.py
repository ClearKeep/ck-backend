from src.services.base import BaseService
from src.models.user import User
from src.models.authen_setting import AuthenSetting
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils
from protos import user_pb2
from utils.logger import *
from msg.message import Message
from src.services.upload_file import UploadFileService
import datetime
from utils.config import get_system_config, get_owner_workspace_domain
from utils.otp import OTPServer
from client.client_user import ClientUser
import base64
import boto3
import os
import hashlib
client_records_list_in_memory = {}


class UserService(BaseService):
    """
    UserService, using when create new user, edit user info, or delete user, or enable/disable mfa flow
    """
    def __init__(self):
        super().__init__(User())
        self.authen_setting = AuthenSetting()

    def create_new_user_srp(self, id, email, password_verifier, salt, iv_parameter, display_name, auth_source):
        # create new normal user with these parameter
        try:
            self.model = User(
                id=id,
                email=email,
                password_verifier=password_verifier,
                salt=salt,
                iv_parameter=iv_parameter,
                display_name=display_name,
                auth_source=auth_source
            )
            self.model.add()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise Exception(Message.REGISTER_USER_FAILED)

    def create_user_social(self, id, email, display_name, auth_source):
        # create new social user with these parameter
        try:
            self.model = User(
                id=id,
                email=email,
                display_name=display_name,
                auth_source=auth_source
            )
            self.model.add()
            return self
        except Exception as e:
            logger.info(e)
            return None

    def forgot_user(self, user_info, new_user_id, password_verifier, salt, iv_parameter):
        # delete user, then recreate user with new user_id and security information
        try:
            self.model = User(
                id=new_user_id,
                email=user_info.email,
                display_name=user_info.display_name,
                auth_source=user_info.auth_source,
                password_verifier=password_verifier,
                salt=salt,
                iv_parameter=iv_parameter,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                status=user_info.status,
                avatar=user_info.avatar,
                phone_number=user_info.phone_number,
                created_at=user_info.created_at
            )
            self.model.add()
            self.delete_user(user_info.id)
        except Exception as e:
            logger.error(e)
            raise Exception(Message.REGISTER_USER_FAILED)

    def get_google_user(self, email, auth_source):
        # get user with email and auth_source info
        user_info = self.model.get_google_user(email, auth_source)
        return user_info

    def change_password(self, request, old_pass, new_pass, user_id):
        # change password in keycloak
        try:
            user_info = self.model.get(user_id)
            response = KeyCloakUtils.set_user_password(user_id, new_pass)

            return user_info
        except Exception as e:
            logger.info(e)
            raise Exception(Message.CHANGE_PASSWORD_FAILED)

    def get_mfa_state(self, user_id):
        # get mfa state of user_id
        user_info = self.model.get(user_id)
        if user_info is None:
            raise Exception(Message.AUTH_USER_NOT_FOUND)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            user_authen_setting = AuthenSetting(id=user_id).add()
        return user_authen_setting.mfa_enable

    def init_mfa_state_enabling(self, user_id):
        # start enable mfa for user_id
        # if otp in frozen state, raising exception
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            user_authen_setting = AuthenSetting(id=user_id).add()
        if user_authen_setting.mfa_enable:
            success = False
            next_step = ''
        else:
            if user_authen_setting.otp_frozen_time > datetime.datetime.now():
                raise Exception(Message.FROZEN_STATE_OTP_SERVICE)

            next_step = 'mfa_validate_password'
            user_authen_setting.require_action = next_step
            user_authen_setting.update()
            success = True
        return success, next_step

    def init_mfa_state_disabling(self, user_id):
        # diable mfa for user_id
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            user_authen_setting = AuthenSetting(id=user_id).add()
        if user_authen_setting.mfa_enable:
            user_authen_setting.mfa_enable = False
            user_authen_setting.update()
            success = True
        else:
            success = False
        next_step = ''
        return success, next_step

    def mfa_validate_password_flow(self, user_id):
        # check if user_id is in mfa_validate_password action
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.require_action != 'mfa_validate_password':
            raise Exception(Message.AUTHEN_SETTING_FLOW_NOT_FOUND)
        return True

    def mfa_request_otp(self, user_id, phone_number):
        # start request otp service for user_id with phone_number
        user_authen_setting = self.authen_setting.get(user_id)
        n_times = user_authen_setting.otp_request_counter + 1
        if n_times > OTPServer.valid_resend_time:
            # reset counter and put otp service into frozen state
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_frozen_time = OTPServer.cal_frozen_time()
            user_authen_setting.update()
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        if user_authen_setting.otp_frozen_time > datetime.datetime.now():
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        try:
            next_step = 'mfa_validate_otp'
            user_authen_setting.require_action = next_step
            hash_otp = OTPServer.get_otp(phone_number)
            user_authen_setting.otp = hash_otp
            user_authen_setting.token_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            success = True
            return success, next_step
        except Exception as e:
            logger.error(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def validate_otp(self, user_id, otp):
        # validate otp service for user_id
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting is None:
            raise Exception(Message.AUTH_USER_NOT_FOUND)
        if user_authen_setting.require_action != 'mfa_validate_otp':
            raise Exception(Message.AUTHEN_SETTING_FLOW_NOT_FOUND)
        if user_authen_setting.otp_tried_time >= OTPServer.valid_trying_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXCEED_MAXIMUM_TRIED_TIMES_OTP)
        if datetime.datetime.now() > user_authen_setting.token_valid_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXPIRED_OTP)
        if OTPServer.check_otp(otp, user_authen_setting.otp) is True:
            user_authen_setting.mfa_enable = True
            user_authen_setting.otp = None
            user_authen_setting.require_action = ""
            user_authen_setting.token_valid_time = datetime.datetime.now()
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.update()
            success = True
            next_step = ''
        else:
            user_authen_setting.otp_tried_time += 1
            user_authen_setting.update()
            raise Exception(Message.WRONG_OTP)
        return success, next_step

    def re_init_otp(self, user_id):
        # retry request otp for user_id
        user_info = self.model.get(user_id)
        if user_info is None:
            raise Exception(Message.AUTH_USER_NOT_FOUND)
        user_authen_setting = self.authen_setting.get(user_id)
        if user_authen_setting.require_action != 'mfa_validate_otp':
            raise Exception(Message.AUTHEN_SETTING_FLOW_NOT_FOUND)
        n_times = user_authen_setting.otp_request_counter + 1
        if n_times > OTPServer.valid_resend_time:
            # reset counter and put otp service into frozen state
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_frozen_time = OTPServer.cal_frozen_time()
            user_authen_setting.update()
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        if user_authen_setting.otp_frozen_time > datetime.datetime.now():
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        try:
            hash_otp = OTPServer.get_otp(user_info.phone_number)
            user_authen_setting.otp = hash_otp
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.token_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            success = True
            next_step = 'mfa_validate_otp'
            return success, next_step
        except Exception as e:
            logger.error(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def update_hash_pass(self, user_id, hash_password, salt='', iv_parameter=''):
        # update hash_password and relate security information for user_id
        user_info = self.model.get(user_id)
        user_info.password_verifier = hash_password
        if salt:
            user_info.salt = salt
        if iv_parameter:
            user_info.iv_parameter = iv_parameter
        user_info.update()
        return (user_info.salt, user_info.iv_parameter)

    def update_hash_pin(self, user_id, hash_pincode, salt='', iv_parameter=''):
        # update hash_pincode and relate security information for user_id
        user_info = self.model.get(user_id)
        user_info.password_verifier = hash_pincode
        if salt:
            user_info.salt = salt
        if iv_parameter:
            user_info.iv_parameter = iv_parameter
        user_info.update()
        return user_info.salt, user_info.iv_parameter

    def get_profile(self, user_id):
        # get profile of user_id
        try:
            user_info = self.model.get(user_id)
            if user_info is not None:
                obj_res = user_pb2.UserProfileResponse(
                    id=user_info.id,
                    display_name=user_info.display_name
                )
                if user_info.email:
                    obj_res.email = user_info.email
                if user_info.phone_number:
                    obj_res.phone_number = user_info.phone_number
                if user_info.avatar:
                    obj_res.avatar = user_info.avatar
                return obj_res
            else:
                return None
        except Exception as e:
            logger.info(e)
            raise Exception(Message.GET_PROFILE_FAILED)

    def update_profile(self, user_id, display_name, phone_number, avatar, clear_phone_number):
        # update profile for user_id, with force clear phone number flag for clearing stored phone number in db
        try:
            profile = self.model.get(user_id)
            if display_name:
                profile.display_name = display_name
            if clear_phone_number:
                user_authen_setting = self.authen_setting.get(user_id)
                if user_authen_setting is None:
                    user_authen_setting = AuthenSetting(id=user_id).add()
                user_authen_setting.enable_mfa = False # change phone_number automatically turn off enable_mfa
                user_authen_setting.update()
                profile.phone_number = ""
            elif phone_number:
                user_authen_setting = self.authen_setting.get(user_id)
                if user_authen_setting is None:
                    user_authen_setting = AuthenSetting(id=user_id).add()
                user_authen_setting.enable_mfa = False # change phone_number automatically turn off enable_mfa
                user_authen_setting.update()
                profile.phone_number = phone_number
            if avatar:
                profile.avatar = avatar
            return profile.update()

        except Exception as e:
            logger.info(e)
            raise Exception(Message.UPDATE_PROFILE_FAILED)

    def get_user_info(self, client_id, workspace_domain):
        # get information of client_id with additional infor about workspace_domain
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
            logger.info(e)
            raise Exception(Message.GET_USER_INFO_FAILED)

    def get_user_by_auth_source(self, email, auth_source):
        # get fully stored information about user by email and auth_source
        user_info = self.model.get_user_by_auth_source(email, auth_source)
        return user_info


    def get_user_by_id(self, client_id):
        # get fully stored information about user by user_id
        user_info = self.model.get(client_id)
        return user_info

    def search_user(self, keyword, client_id):
        # searching user with keyword differ to client_id
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
            logger.info(e, exc_info=True)
            raise Exception(Message.SEARCH_USER_FAILED)

    def get_users(self, client_id, workspace_domain):
        # get other users for client_id within workspace_domain
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
            logger.info(e)
            raise Exception(Message.GET_USER_INFO_FAILED)

    def find_user_by_email(self, email_hash):
        try:
            logger.debug(f'Finding user by email, {email_hash=}')


            # TODO: delete these comments after CLK32-909
            # import hashlib
            #
            #
            # logger.debug(f'Getting users, experimenting')
            #
            # owner_workspace_domain = get_owner_workspace_domain()
            #
            # all_users = self.model.get_all_users()
            # for u in all_users:
            #     if type(u.email) is str:
            #         logger.debug(  (hashlib.sha256(u.email.encode('ascii')).hexdigest(), owner_workspace_domain)   )
            #
            #



            self.push_all_users_email_hash_to_orbitdb_network()


            # =============MOCKS===========================
            # TODO: IMP/fix these mocks

            mock_email_list = ["user0@email_server0.com",
                               "user1@email_server1.com",
                               "user2@email_server2.com"]
            import hashlib
            email_hash_list = [hashlib.sha256(email.encode('ascii')).hexdigest() for email in mock_email_list]

            mock_list_of_user_info = {
                email_hash_list[0]: [
                    {
                        "id": "6092b16d-4d81-4270-9423-76367ab4b6ac",
                        "displayName": "Nguy\u1EC5n Th\u1ECB Trang dev",
                        "workspaceDomain": "54.235.68.160:25000"
                    },
                    {
                        "id": "8cc42f22-f7c4-43ba-987a-af2f886c13c1",
                        "displayName": "L\u01B0\u01A1ng Th\u1ECB Thu Ph\u01B0\u01A1ng (Emily)",
                        "workspaceDomain": "54.235.68.160:25000"
                    }
                ],
                email_hash_list[1]: [{
                    "id": "773ff88e-7673-4946-8a69-fd77505a65c6",
                    "displayName": "Obamaygggvvcc",
                    "workspaceDomain": "54.235.68.160:25000"
                }],
                email_hash_list[2]: [
                    {
                        "id": "c551b558-b054-4246-b440-c295db4d561d",
                        "displayName": "Phuong",
                        "workspaceDomain": "54.235.68.160:25000"
                    },
                    {
                        "id": "3b5ea2d2-bb64-49c8-b2aa-e9b8226de329",
                        "displayName": "Xuan An Tong",
                        "workspaceDomain": "54.235.68.160:25000"
                    },
                    {
                        "id": "eb668747-4256-4292-943b-4ef2bc368f38",
                        "displayName": "tt",
                        "workspaceDomain": "54.235.68.160:25000"
                    },
                    {
                        "id": "998caf43-e398-4df1-b993-6830eef989e8",
                        "displayName": "Ph\u1EA1m T\u1EA5t Th\u00E0nh",
                        "workspaceDomain": "54.235.68.160:25000"
                    }
                ]
            }

            try:
                lst_user = mock_list_of_user_info[email_hash]
            except KeyError:
                lst_user = []

            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj['id'],
                    display_name=obj['displayName'],
                    workspace_domain=obj['workspaceDomain']
                )
                lst_obj_res.append(obj_res)

            # TODO: IMP/fix these mocks
            # =============END MOCKS===========================

            return user_pb2.FindUserByEmailResponse(lst_user=lst_obj_res)



        except Exception:
            logger.info('Error while finding user by email', exc_info=True)
            raise Exception(Message.FIND_USER_BY_EMAIL_FAILED)

    def push_all_users_email_hash_to_orbitdb_network(self):
        try:
            # TODO: find different way to do this
            logger.debug(f'Push all users to orbit-db network')

            owner_workspace_domain = get_owner_workspace_domain()

            all_users = self.model.get_all_users()
            for u in all_users:
                if type(u.email) is str:
                    logger.debug(  (hashlib.sha256(u.email.encode('ascii')).hexdigest(), owner_workspace_domain)   )





        except Exception:
            logger.error("Error while push users to orbit-db network", exc_info=True)

    def update_last_login(self, user_id):
        # update last time login for user_id
        try:
            user_info = self.model.get(user_id)
            user_info.last_login_at = datetime.datetime.now()
            user_info.update()
        except Exception as e:
            logger.info(e)

    def set_user_status(self, client_id, status):
        # set status for client_id
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
        # update client record in temp variable
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
        # create and return categorize_workspace_domains, with client is devided into each workspace
        workspace_domains_dictionary = {}

        for client in list_clients:
            if str(client.workspace_domain) in workspace_domains_dictionary.keys():
                workspace_domains_dictionary[str(client.workspace_domain)].append(client)
            else:
                workspace_domains_dictionary.update({
                    str(client.workspace_domain): [client]
                })
        return workspace_domains_dictionary

    def get_list_clients_status(self, list_clients, should_get_profile):
        # get list of clients status, with returning additional basic infor of user is should_get_profile is True
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
                        if should_get_profile:
                            user_info = self.model.get(client.client_id)
                            if user_info is not None:
                                if user_info.display_name:
                                    tmp_client_response.display_name = user_info.display_name
                                if user_info.phone_number:
                                    tmp_client_response.phone_number = user_info.phone_number
                                if user_info.avatar:
                                    tmp_client_response.avatar = user_info.avatar
                            logger.info("user info {}: {}".format(client.client_id, tmp_client_response))
                        list_clients_status.append(tmp_client_response)
                else:
                    logger.info("workspace request other server {}".format(workspace_domain))
                    other_clients_response = self.get_other_workspace_clients_status(workspace_domain, list_client, should_get_profile)
                    list_clients_status.extend(other_clients_response)

            response = user_pb2.GetClientsStatusResponse(
                lst_client=list_clients_status
            )
            return response
        except Exception as e:
            logger.error(e)
            raise Exception(Message.GET_USER_STATUS_FAILED)



    def get_owner_workspace_client_status(self, client_id):
        # get client record of client_id in this server
        client_record = client_records_list_in_memory.get(str(client_id), None)

        if client_record is not None:
            leave_time_amount = datetime.datetime.now() - client_record["last_active"]

            if leave_time_amount.seconds > get_system_config().get("maximum_offline_time_limit"):
                user_status = "Offline"
            else:
                if client_record["user_status"] is not None:
                    user_status = client_record["user_status"]
                else:
                    user_status = "Online"
        else:
            user_status = "Undefined"
        return user_status

    def get_other_workspace_clients_status(self, workspace_domain, list_client, should_get_profile=False):
        # get client record of client_id in other server
        server_error_resp = []

        client = ClientUser(workspace_domain)
        client_resp = client.get_clients_status(list_client, should_get_profile)

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

    def base64_enconding_text_to_string(self, text):
        # encode utf-8 string to ascii string
        text_bytes = text.encode("ascii")
        encoded_text_bytes = base64.b64encode(text_bytes)
        return encoded_text_bytes.decode('ascii')

    def upload_avatar(self, client_id, file_name, file_content, file_type, file_hash):
        # upload avatar for client_id
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3 and resize if needed
        tmp_file_name, file_ext = os.path.splitext(file_name)
        avatar_file_name = self.base64_enconding_text_to_string(client_id) + file_ext

        avatar_url = UploadFileService().upload_to_s3(avatar_file_name, file_content, file_type)
        obj_res = user_pb2.UploadAvatarResponse(
            file_url=avatar_url
        )
        return obj_res

    def delete_user(self, user_id):
        # delete user, note that this function must be called only by admin
        user_info = self.model.get(user_id)
        user_info.delete()
        return True
