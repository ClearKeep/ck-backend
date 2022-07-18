import time
import datetime
import requests
from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *
from src.services.notify_push import NotifyPushService, PushType
import json
from src.services.user import UserService
from src.models.base import Database
from src.models.user import User
from src.models.authen_setting import AuthenSetting
from utils.otp import OTPServer
from utils.smtp import MailerServer
from utils.config import get_system_config, get_owner_workspace_domain
import logging
logger = logging.getLogger(__name__)

class AuthService:
    """
    Authen Service for authenticate action. This service involved in any granted authentication, include register new user,
    login, logout, forgot password, generate pre_access_token or start mfa service.
    """
    def __init__(self):
        super().__init__()
        self.user_db = User()
        self.authen_setting = AuthenSetting()

    def token(self, user_name, password):
        # basic authen service for login with user_name and password
        try:
            token = KeyCloakUtils.token(user_name, password)
            if token:
                return token
        except Exception as e:
            logger.info(e)
            response_code = e.response_code
            check_error = json.loads(e.args[0]).get("error")
            if check_error == "invalid_grant" and response_code == 400:
                raise Exception(Message.USER_NOT_VERIFY_EMAIL)
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def logout(self, refresh_token):
        # basic authen service for logout using refresh_token
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

    async def forgot_user(self, email, password_verifier, display_name):
        try:
            # delete user, then re create new user with activate status is True
            old_user_id = self.get_user_by_email(email)["id"]
            push_service = NotifyPushService()
            data = {
                    'client_id': old_user_id,
                    'deactive_account_id': old_user_id
                }
            await push_service.push_text_to_client(
                to_client_id=old_user_id,
                title="Deactivate Member",
                body="A user has been deactived",
                from_client_id=old_user_id,
                notify_type=PushType.DEACTIVE_ACCOUNT.value,
                data=json.dumps(data)
            )
            self.delete_user(old_user_id)
            new_user_id = KeyCloakUtils.create_user(email, email, password_verifier, "", display_name)
            if new_user_id:
                KeyCloakUtils.active_user(new_user_id)
                return new_user_id
        except Exception as e:
            logger.info(e)
            raise Exception(Message.REGISTER_USER_FAILED)

    def register_srp_user(self, email, password_verifier, display_name):
        # register new user with using email as user name
        try:
            user_id = KeyCloakUtils.create_user(email, email, password_verifier, "", display_name)
            if user_id:
                a = KeyCloakUtils.send_verify_email(user_id)
                return user_id
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception(Message.REGISTER_USER_FAILED)

    def delete_user(self, userid):
        # delete user in keycloak server by its userid
        try:
            KeyCloakUtils.delete_user(user_id=userid)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.UNAUTHENTICATED)


    def get_user_by_email(self, email):
        # get user in keycloak server by its email
        try:
            return KeyCloakUtils.get_user_by_email(email)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.USER_NOT_FOUND)

    def send_forgot_password(self, email):
        # send an email to user with app link for reset password
        try:
            user = self.get_user_by_email(email=email)
            if not user:
                raise Exception(Message.USER_NOT_FOUND)
        except Exception as e:
            logger.info(e)
            raise Exception(Message.USER_NOT_FOUND)
        else:
            pre_access_token = self.hash_pre_access_token(user['id'], "forgot_password")
            server_domain = get_owner_workspace_domain()
            user_info = User().get(user['id'])
            if user_info.auth_source == 'account':
                MailerServer.send_reset_password_mail(email, email, pre_access_token, server_domain)
                return user['id']
            else:
                raise Exception(Message.EMAIL_ALREADY_USED_FOR_SOCIAL_SIGNIN)

    # login google
    def google_login(self, google_id_token):
        # google login by using google id token, return user_name, user_id and boolean variable indicate if this user is new user
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
            user = self.get_user_by_email(email=google_email)
            #active_user
            if user:
                if not user["emailVerified"]:
                    KeyCloakUtils.active_user(user["id"])
                user_info = UserService().get_user_by_id(user["id"])
                return google_email, user["id"], user_info.password_verifier is None or user_info.password_verifier == ""
            else:
                # create new user
                new_user_id = KeyCloakUtils.create_user_without_password(google_email, google_email, "", google_token_info["name"])
                new_user = UserService().create_user_social(id=new_user_id, email=google_email,
                                                          display_name=google_token_info["name"],
                                                          auth_source='google')
                if new_user is None:
                    self.delete_user(new_user_id)
                    raise Exception(Message.REGISTER_USER_FAILED)
                return google_email, new_user_id, True
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception(Message.GOOGLE_AUTH_FAILED)

    # login office
    def office_login(self, office_access_token):
        # office login by using office access token, return user_name, user_id and boolean variable indicate if this user is new user
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
            user = self.get_user_by_email(office_id)
            if user:
                user_info = UserService().get_user_by_id(user["id"])
                return office_id, user["id"], user_info.password_verifier is None or user_info.password_verifier == ""
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
                return office_id, new_user_id, True
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception(Message.OFFICE_AUTH_FAILED)

    # login facebook
    def facebook_login(self, facebook_access_token):
        # facebook login by using facebook access token, return user_name, user_id and boolean variable indicate if this user is new user
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
            user = self.get_user_by_email(facebook_id)
            if user:
                user_info = UserService().get_user_by_id(user["id"])
                return facebook_id, user["id"], user_info.password_verifier is None or user_info.password_verifier == ""
            else:
                # create new user
                new_user_id = KeyCloakUtils.create_user_without_password(facebook_email, facebook_id, "", facebook_name)
                new_user = UserService().create_user_social(id=new_user_id, email=facebook_email,
                                                          display_name=facebook_name,
                                                          auth_source='facebook')
                if new_user is None:
                    self.delete_user(new_user_id)
                    raise Exception(Message.REGISTER_USER_FAILED)
                return facebook_id, new_user_id, True
        except Exception as e:
            logger.info(e)
            raise Exception(Message.FACEBOOK_AUTH_FAILED)

    def create_otp_service(self, client_id):
        # start opt service for client if mfa is enabled, raising FROZEN_STATE_OTP_SERVICE if mfa is enabled and in frozen state (request resend otp too many times)
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
            hash_otp = OTPServer.get_otp(user_info.phone_number)
            user_authen_setting.otp = hash_otp
            user_authen_setting.token_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            success = True
            # we create hash_key with valid_time to make hash_key will change each request
            hash_key = OTPServer.hash_uid(client_id, user_authen_setting.token_valid_time)
            return hash_key
        except Exception as e:
            logger.info(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def verify_otp(self, client_id, hash_key, otp):
        # verify opt for client if mfa is enabled, raising FROZEN_STATE_OTP_SERVICE if mfa is enabled and in frozen state (request resend otp too many times)
        # if client try to verify an otp too many times, this otp will become invalid
        user_authen_setting = self.authen_setting.get(client_id)
        if user_authen_setting is None:
            raise Exception(Message.GET_MFA_STATE_FALED)
        success = OTPServer.verify_hash_code(client_id, user_authen_setting.token_valid_time, hash_key)
        if not success:
            raise Exception(Message.GET_VALIDATE_HASH_OTP_FAILED)
        if user_authen_setting.otp_tried_time >= OTPServer.valid_trying_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXCEED_MAXIMUM_TRIED_TIMES_OTP)
        if datetime.datetime.now() > user_authen_setting.token_valid_time:
            user_authen_setting.otp = None
            user_authen_setting.update()
            raise Exception(Message.EXPIRED_OTP)
        if OTPServer.check_otp(otp, user_authen_setting.otp) is False:
            user_authen_setting.otp_tried_time += 1
            user_authen_setting.update()
            raise Exception(Message.WRONG_OTP)
        else:
            user_authen_setting.otp = None
            user_authen_setting.token_valid_time = datetime.datetime.now()
            user_authen_setting.otp_request_counter = 0
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.update()
        return success

    def resend_otp(self, client_id, hash_key):
        # resend opt for client if mfa is enabled, raising FROZEN_STATE_OTP_SERVICE if mfa is enabled and in frozen state (request resend otp too many times)
        user_authen_setting = self.authen_setting.get(client_id)
        if user_authen_setting is None:
            logger.info(Message.GET_MFA_STATE_FALED)
            raise Exception(Message.GET_MFA_STATE_FALED)
        success = OTPServer.verify_hash_code(client_id, user_authen_setting.token_valid_time, hash_key)
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
            hash_otp = OTPServer.get_otp(user_info.phone_number)
            user_authen_setting.otp = hash_otp
            user_authen_setting.otp_tried_time = 0
            user_authen_setting.token_valid_time = OTPServer.get_valid_time()
            user_authen_setting.otp_request_counter = n_times
            user_authen_setting.update()
            # we create hash_key with valid_time to make hash_key will change each request
            hash_key = OTPServer.hash_uid(client_id, user_authen_setting.token_valid_time)
            return hash_key
        except Exception as e:
            logger.info(e)
            raise Exception(Message.OTP_SERVER_NOT_RESPONDING)

    def hash_pre_access_token(self, user_name, require_action):
        # create a pre access_token by signing a jws with user_name as iss, require_action as aud
        hash_key = OTPServer.sign_message(user_name, require_action)
        return hash_key

    def verify_hash_pre_access_token(self, user_name, signed_message, require_action):
        # verify a pre access_token signed by jws with user_name as iss, require_action as aud
        try:
            message = OTPServer.verify_message(signed_message)
            if message.get("iss", None) != user_name:
                return False
            if message.get("aud", None) != require_action:
                return False
            if message.get("exp", 0) < int(time.time()):
                return False
            return True
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    async def notify_myself_reset_pincode(self, user_id):
        push_service = NotifyPushService()
        data = {
                'user_id': user_id,
                'reset_pincode_user_id': user_id
            }
        await push_service.push_text_to_client(
            to_client_id=user_id,
            title="Reset pincode",
            body="A user has been reset pincode",
            from_client_id=user_id,
            notify_type=PushType.RESET_PINCODE.value,
            data=json.dumps(data)
        )

    def refresh_token(self, refresh_token):
        token = KeyCloakUtils.refresh_token(refresh_token)
        return token
