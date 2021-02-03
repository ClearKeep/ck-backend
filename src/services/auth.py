from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *
from src.models.notify_token import NotifyToken
from src.services.notify_push import NotifyPushService

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
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def refresh_token(self, email, password):
        try:
            token = self.token(email,password)
            refresh_token = KeyCloakUtils.refresh_token(token['refresh_token'])
            if refresh_token:
                return refresh_token
            else:
                return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.AUTH_USER_NOT_FOUND)

    def logout(self, email=None, password=None, refresh_token=None):
        try:
            if refresh_token:
                KeyCloakUtils.logout(refresh_token)
            else:
                token = self.token(email, password)
                KeyCloakUtils.logout(token['refresh_token'])
            if token:
                return token
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    def remove_token(self, client_id, device_id):
        try:
            NotifyPushService().delete_token(client_id=client_id,device_id=device_id)
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
            rkeycloak_admin.delete_user(user_id=userid)
            if newUserId:
                return newUserId
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UNAUTHENTICATED)

    #param: name or email
    def get_user_id_by_email(self, email):
        try:
            return KeyCloakUtils.get_user_id_by_email(email)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)

    def send_forgot_password(self,email):
        try:
            user_id = self.get_user_id_by_email(email=email)
            if user_id:
                KeyCloakUtils.send_forgot_password(user_id=user_id,email=email)
                return user_id
            else:
                # logger.info(bytes(str(e), encoding='utf-8'))
                raise Exception(Message.USER_NOT_FOUND)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)
