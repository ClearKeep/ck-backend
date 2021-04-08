from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *
from src.services.notify_push import NotifyPushService
import json
from src.services.user import UserService
from utils.config import get_system_config
import requests


class AuthService:
    def __init__(self):
        super().__init__()

    def token(self, email, password):
        try:
            token = KeyCloakUtils.token(email, password)
            if token:
                return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
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
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def logout(self, refresh_token):
        try:
            KeyCloakUtils.logout(refresh_token)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    def remove_token(self, client_id, device_id):
        try:
            NotifyPushService().delete_token(client_id=client_id, device_id=device_id)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    def register_user(self, email, password, display_name):
        try:
            user_id = KeyCloakUtils.create_user(email, password, "", display_name)
            KeyCloakUtils.send_verify_email(user_id)
            if user_id:
                return user_id
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def delete_user(self, userid):
        try:
            KeyCloakUtils.delete_user(user_id=userid)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    # param: name or email
    def get_user_id_by_email(self, email):
        try:
            return KeyCloakUtils.get_user_id_by_email(email)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)

    def send_forgot_password(self, email):
        try:
            user_id = self.get_user_id_by_email(email=email)
            if user_id:
                KeyCloakUtils.send_forgot_password(user_id=user_id, email=email)
                return user_id
            else:
                raise Exception(Message.USER_NOT_FOUND)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)

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
            if google_token_info["aud"] != google_app_id["ios"] and google_token_info["aud"] != google_app_id[
                "android"]:
                raise Exception(Message.GOOGLE_AUTH_FAILED)

            google_email = google_token_info["email"]
            # check account exits
            user_id = KeyCloakUtils.get_user_id_by_email(google_email)
            if user_id:
                token = self.exchange_token(user_id)
                return token
            else:
                # create new user
                new_user_id = KeyCloakUtils.create_user_with_email(google_email, "", google_token_info["name"])
                token = self.exchange_token(new_user_id)
                UserService().create_user_with_last_login(id=new_user_id, email=google_email,
                                                          display_name=google_token_info["name"],
                                                          auth_source='google')
                return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
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
            user_id = KeyCloakUtils.get_user_id_by_email(office_id)
            if user_id:
                token = self.exchange_token(user_id)
                return token
            else:
                display_name = office_token_info["displayName"]
                if not display_name:
                    if office_token_info["userPrincipalName"]:
                        user_principal_name = office_token_info["userPrincipalName"].split("@")
                        if len(user_principal_name) > 0:
                            display_name = user_principal_name[0]
                # create new user
                new_user_id = KeyCloakUtils.create_user_with_username(office_id, "", display_name)
                token = self.exchange_token(new_user_id)
                UserService().create_user_with_last_login(id=new_user_id, email=office_token_info["mail"],
                                                          display_name=display_name,
                                                          auth_source='office')
                return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.OFFICE_AUTH_FAILED)

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
