import datetime
from hashlib import md5
from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *
from src.services.notify_push import NotifyPushService
import json
from src.services.user import UserService
from src.models.base import Database
from src.models.user import User
from src.models.authen_setting import AuthenSetting
from utils.config import get_system_config
from utils.otp import OTPServer
import requests


class AuthService:
    def __init__(self):
        super().__init__()
        self.user_db = User()
        self.authen_setting = AuthenSetting()

    def token(self, email, password):
        try:
            token = KeyCloakUtils.token(email, password)
            if token:
                return token
        except Exception as e:
            logger.info(e)
            response_code = e.response_code
            check_error = json.loads(e.args[0]).get("error")
            if check_error == "invalid_grant" and response_code == 400:
                raise Exception(Message.USER_NOT_VERIFY_EMAIL)
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def refresh_token(self, email, password):
        try:
            token = self.token(email, password)
            refresh_token = KeyCloakUtils.refresh_token(token['refresh_token'])
            if refresh_token:
                return refresh_token
            else:
                return token
        except Exception as e:
            logger.info(e)
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def logout(self, refresh_token):
        try:
            KeyCloakUtils.logout(refresh_token)
        except Exception as e:
            logger.info(e)
            # raise Exception(Message.UNAUTHENTICATED)

    def remove_token(self, client_id, device_id):
        try:
            NotifyPushService().delete_token(client_id=client_id, device_id=device_id)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.UNAUTHENTICATED)

    def register_user(self, email, password, display_name):
        try:
            user_id = KeyCloakUtils.create_user(email, email, password, "", display_name)
            a = KeyCloakUtils.send_verify_email(user_id)
            if user_id:
                return user_id
        except Exception as e:
            logger.info(e)
            return None

    def delete_user(self, userid):
        try:
            KeyCloakUtils.delete_user(user_id=userid)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.UNAUTHENTICATED)


    def get_user_by_email(self, email):
        try:
            return KeyCloakUtils.get_user_by_email(email)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.USER_NOT_FOUND)

    def send_forgot_password(self, email):
        try:
            user = self.get_user_by_email(email=email)
            if not user:
                raise Exception(Message.USER_NOT_FOUND)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.USER_NOT_FOUND)
        else:
            auth_source = Database.get_session().query(User) \
                .filter(User.id == user['id']) \
                .filter(User.last_login_at != None) \
                .all()[0] \
                .auth_source
            Database.get().session.remove()
            if auth_source == 'account':
                KeyCloakUtils.send_forgot_password(user_id=user["id"], email=email)
                return user['id']
            else:
                raise Exception(Message.EMAIL_ALREADY_USED_FOR_SOCIAL_SIGNIN)

    # login google
    def google_login(self, google_id_token):
        try:
            verify_id_token_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + google_id_token
            req = requests.get(url=verify_id_token_url)
            if req.status_code != 200:
                raise Exception(Message.GOOGLE_AUTH_ID_TOKEN_INVALID)
            google_token_info = req.json()

            logger.info("Google login token spec:")
            logger.info(google_token_info)

            # check google_token_info["aud"] matching with google app id
            google_app_id = get_system_config()["google_app_id"]
            if google_token_info["aud"] != google_app_id["ios"] and google_token_info["aud"] != google_app_id["android"]:
                raise Exception(Message.GOOGLE_AUTH_FAILED)

            google_email = google_token_info["email"]
            # check account exits
            user_id, user_exist = self.get_user_by_email(email=google_email) #UserService().get_google_user(google_email, "google")
            #active_user
            if user_exist:
                if not user_exist["emailVerified"]:
                    KeyCloakUtils.active_user(user_exist["id"])
                pincode = UserService().get_pincode(user_id)
                return user_id, google_email, pincode is None or pincode == ""
            else:
                # create new user
                new_user_id = KeyCloakUtils.create_user_without_password(google_email, google_email, "", google_token_info["name"])
                new_user = UserService().create_user_social(id=new_user_id, email=google_email,
                                                          display_name=google_token_info["name"],
                                                          auth_source='google')
                if new_user is None:
                    self.delete_user(new_user_id)
                    raise Exception(Message.REGISTER_USER_FAILED)
                return new_user_id, google_email, True
        except Exception as e:
            logger.info(e)
            raise Exception(Message.GOOGLE_AUTH_FAILED)

    # login office
    def office_login(self, office_access_token):
        try:
            verify_token_url = "https://graph.microsoft.com/v1.0/me"
            bearer = 'Bearer ' + office_access_token
            headers = {'Authorization': bearer}

            req = requests.get(url=verify_token_url, headers=headers)
            if req.status_code != 200:
                raise Exception(Message.OFFICE_ACCESS_TOKEN_INVALID)
            office_token_info = req.json()

            logger.info("Office login token spec:")
            logger.info(office_token_info)

            office_id = office_token_info["id"]
            # check account exits
            user_id, user = KeyCloakUtils.get_user_by_email(office_id)
            if user:
                pincode = UserService().get_pincode(user_id)
                return user_id, office_id, pincode is None or pincode == ""
            else:
                display_name = office_token_info["displayName"]
                email = ""
                if not display_name:
                    if office_token_info["userPrincipalName"]:
                        user_principal_name = office_token_info["userPrincipalName"].split("@")
                        if len(user_principal_name) > 0:
                            display_name = user_principal_name[0]
                            email = office_token_info["userPrincipalName"]
                # create new user
                new_user_id = KeyCloakUtils.create_user_without_password(email, office_id, "", display_name)
                new_user = UserService().create_user_social(id=new_user_id, email=office_token_info["mail"],
                                                          display_name=display_name,
                                                          auth_source='office')
                if new_user is None:
                    self.delete_user(new_user_id)
                    raise Exception(Message.REGISTER_USER_FAILED)
                return new_user_id, office_id, True
        except Exception as e:
            logger.info(e)
            raise Exception(Message.OFFICE_AUTH_FAILED)

    # login facebook
    def facebook_login(self, facebook_access_token):
        try:
            # validate access_token
            facebook_app_id = get_system_config()["facebook_app"]
            verify_token_app_id = "https://graph.facebook.com/debug_token?input_token={}&access_token={}|{}".format(
                facebook_access_token, facebook_app_id["app_id"], facebook_app_id["app_secret"])
            req = requests.get(url=verify_token_app_id)
            if req.status_code != 200:
                raise Exception(Message.FACEBOOK_ACCESS_TOKEN_INVALID)
            facebook_token_app_id_info = req.json()
            facebook_token_app_id = facebook_token_app_id_info["data"]["app_id"]
            if facebook_token_app_id != facebook_app_id["app_id"]:
                raise Exception(Message.FACEBOOK_ACCESS_TOKEN_INVALID)

            verify_token_url = "https://graph.facebook.com/me?fields=id,name,email&access_token=" + facebook_access_token
            req = requests.get(url=verify_token_url)

            if req.status_code != 200:
                raise Exception(Message.FACEBOOK_ACCESS_TOKEN_INVALID)
            facebook_token_info = req.json()

            logger.info("Facebook login token spec:")
            logger.info(facebook_token_info)

            facebook_id = facebook_token_info["id"]
            facebook_email = facebook_token_info["email"]
            facebook_name = facebook_token_info["name"]
            # check account exits
            user_id, user = KeyCloakUtils.get_user_by_email(facebook_id)
            if user:
                pincode = UserService().get_pincode(user_id)
                return facebook_id, pincode is None or pincode == ""
            else:
                # create new user
                new_user_id = KeyCloakUtils.create_user_without_password(facebook_email, facebook_id, "", facebook_name)
                new_user = UserService().create_user_social(id=new_user_id, email=facebook_email,
                                                          display_name=facebook_name,
                                                          auth_source='facebook')
                if new_user is None:
                    self.delete_user(new_user_id)
                    raise Exception(Message.REGISTER_USER_FAILED)
                return new_user_id, facebook_id, True
        except Exception as e:
            logger.info(e)
            raise Exception(Message.FACEBOOK_AUTH_FAILED)

    def exchange_token(self, user_id):
        config_keycloak_admin = get_system_config()['keycloak_admin']
        exchange_token_url = "{auth_server_url}realms/{realm_name}/protocol/openid-connect/token".format(
            auth_server_url=config_keycloak_admin['server_url'], realm_name=config_keycloak_admin['realm_name'])

        # generate token for impersonator
        impersonator_token_data = {'grant_type': 'password',
                                   'client_id': config_keycloak_admin['client_id'],
                                   'username': config_keycloak_admin['username'],
                                   'password': config_keycloak_admin['password'],
                                   'client_secret': config_keycloak_admin['client_secret_key']}
        req = requests.post(url=exchange_token_url, data=impersonator_token_data)
        if req.status_code != 200:
            return None
        impersonator_token = req.json()

        # exchange token for specific user
        target_user_token_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
                                  'client_id': "admin-cli",
                                  'requested_subject': user_id,
                                  'subject_token': impersonator_token["access_token"],
                                  'client_secret': config_keycloak_admin['client_secret_key']}
        req = requests.post(url=exchange_token_url, data=target_user_token_data)
        if req.status_code == 200:
            user_token_info = req.json()
            return user_token_info
        else:
            return None

    def create_otp_service(self, client_id):
        user_info = self.user_db.get(client_id)
        user_authen_setting = self.authen_setting.get(client_id)
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
            otp = OTPServer.get_otp(user_info.phone_number)
            user_authen_setting.otp = otp
            user_authen_setting.otp_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            success = True
            # we create hash_key with valid_time to make hash_key will change each request
            hash_key = OTPServer.hash_uid(client_id, user_authen_setting.otp_valid_time)
            return hash_key
        except Exception as e:
            logger.info(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def verify_otp(self, client_id, hash_key, otp):
        user_authen_setting = self.authen_setting.get(client_id)
        if user_authen_setting is None:
            raise Exception(Message.GET_MFA_STATE_FALED)
        success = OTPServer.verify_hash_code(client_id, user_authen_setting.otp_valid_time, hash_key)
        if not success:
            raise Exception(Message.GET_VALIDATE_HASH_OTP_FAILED)
        if user_authen_setting.otp_tried_time >= OTPServer.valid_trying_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXCEED_MAXIMUM_TRIED_TIMES_OTP)
        if datetime.datetime.now() > user_authen_setting.otp_valid_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXPIRED_OTP)
        if otp != user_authen_setting.otp:
            user_authen_setting.otp_tried_time += 1
            user_authen_setting.update()
            raise Exception(Message.WRONG_OTP)
        else:
            user_authen_setting.otp = None
            user_authen_setting.otp_valid_time = datetime.datetime.now()
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.update()
            token = self.exchange_token(client_id)
        return success, token

    def resend_otp(self, client_id, hash_key):
        user_authen_setting = self.authen_setting.get(client_id)
        if user_authen_setting is None:
            logger.info(Message.GET_MFA_STATE_FALED)
            raise Exception(Message.GET_MFA_STATE_FALED)
        success = OTPServer.verify_hash_code(client_id, user_authen_setting.otp_valid_time, hash_key)
        if not success:
            logger.info(Message.GET_VALIDATE_HASH_OTP_FAILED)
            raise Exception(Message.GET_VALIDATE_HASH_OTP_FAILED)
        n_times = user_authen_setting.otp_request_counter + 1
        if n_times > OTPServer.valid_resend_time:
            # reset counter and put otp service into frozen state
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_frozen_time = OTPServer.cal_frozen_time()
            user_authen_setting.update()
            logger.info(Message.FROZEN_STATE_OTP_SERVICE)
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        if user_authen_setting.otp_frozen_time > datetime.datetime.now():
            raise Exception(Message.FROZEN_STATE_OTP_SERVICE)
        try:
            user_info = self.user_db.get(client_id)
            otp = OTPServer.get_otp(user_info.phone_number)
            user_authen_setting.otp = otp
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.otp_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            # we create hash_key with valid_time to make hash_key will change each request
            hash_key = OTPServer.hash_uid(client_id, user_authen_setting.otp_valid_time)
            return hash_key
        except Exception as e:
            logger.info(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def hash_pre_access_token(self, client_id, user_name, require_action):
        # lend the hash_uid from utils.otp
        hash_key, message = OTPServer.sign_message(client_id, user_name, require_action)
        return hash_key

    def verify_hash_pre_access_token(self, user_id, signed_message, require_action):
        try:
            message = OTPServer.verify_message(signed_message)
            if message.get("aud", None) != require_action:
                return False, ""
            if message.get("kid", "")  != user_id:
                return False, ""
            return True, message.get("iss", "")
        except Exception as e:
            logger.error(e)
            return False, ""
