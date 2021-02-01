from msg.message import Message
from utils.keycloak import KeyCloakUtils
from utils.logger import *


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

    def register_user(self, email, password):
        try:
            newUserId = KeyCloakUtils.create_user(email, password)
            KeyCloakUtils.send_verify_email(newUserId)
            if newUserId:
                return newUserId
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    #param: name or email
    def get_user_id_by_email(self, email):
        try:
            return KeyCloakUtils.get_user_id_by_email(email)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)

    def send_forgot_password(self,email):
        try:
            Userid = self.get_user_id_by_email(email=email)
            if Userid:
                KeyCloakUtils.send_forgot_password(user_id=Userid,email=email)
                return Userid
            else:
                logger.info(bytes(str(e), encoding='utf-8'))
                raise Exception(Message.USER_NOT_FOUND)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.USER_NOT_FOUND)
