from src.services.base import BaseService
from src.models.user import User
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils

class SimpleException(Exception):
    def __init__(self, errors):
        self.errors = errors  # list of ApiError

class UserService(BaseService):
    def __init__(self):
        super().__init__(User())

    def create_new_user(self, id, record, auth_source):
        self.model = User(
            id=id,
            email=EncryptUtils.encrypt_data(record.email, record.password, id),
            username=record.username,
            first_name=EncryptUtils.encrypt_data(record.first_name, record.password, id),
            last_name=EncryptUtils.encrypt_data(record.last_name, record.password, id),
            auth_source=auth_source
        )
        return self.model.add()

    def change_password(self, request, old_pass, new_pass, user_id):
        try:
            user_info = self.find_by_id(user_id)

            response = KeyCloakUtils.set_user_password(user_id, new_pass)
            
            email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
            first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
            last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)

            user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
            user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
            user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)

            return user_info.update()
        except Exception as e:
            print(e)
            raise SimpleException('change password error')

    def get_user_info(self, user_id, hash_key):
        try:
            user_info = self.find_by_id(user_id)
            email = EncryptUtils.decrypt_with_hash(user_info.email, hash_key)
            first_name = EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key)
            last_name = EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key)

            user_info.email = email
            user_info.first_name = first_name
            user_info.last_name = last_name
            return user_info

        except Exception as e:
            print(e)
            raise SimpleException('get user info error')

    def update_user_info(self,request, user_id, hash_key):
        print("update_user_info service")

