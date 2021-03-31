from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *
from src.services.notify_push import NotifyPushService
import json
import requests
from src.services.user import UserService
from utils.config import get_system_config


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

    def register_user(self, email, password):
        try:
            user_id = KeyCloakUtils.create_user(email, password)
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
            if req.status_code != "200":
                raise Exception(Message.GOOGLE_AUTH_ID_TOKEN_INVALID)
            google_token_info = req.json()

            # check google_token_info["aud"] matching with google app id
            google_app_id = get_system_config["google_app_id"]
            if google_token_info["aud"] != google_app_id["ios"] and google_token_info["aud"] != google_app_id["android"]:
                raise Exception(Message.GOOGLE_AUTH_FAILED)

            google_email = google_token_info["email"]
            # check account exits
            user_id = KeyCloakUtils.get_user_id_by_email()
            if not user_id:
                # create new user
                new_user_id = KeyCloakUtils.create_user_with_email(google_email)
                UserService().create_new_user(new_user_id, google_email, new_user_id, google_token_info["given_name"],
                                              google_token_info["family_name"], google_token_info["name"], 'google')
            # generate token
            token = KeyCloakUtils.exchange_token(user_id)
            return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GOOGLE_AUTH_FAILED)
