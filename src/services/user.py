from src.services.base import BaseService
from src.models.user import User
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils

# class SimpleException(Exception):
#     def __init__(self, errors):
#         self.errors = errors  # list of ApiError

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
        # print('asmdwwww====>>>ad')
        try:
            response = KeyCloakUtils.set_user_password(user_id, new_pass)
            print(response)
        except Exception as e:
            print(e)

        # user_info = self.find_by_id(user_id)
    
        # email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
        # first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
        # last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)

        # user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
        # user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
        # user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)
        # return user_info.update()
        # try:
        #     email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
        # except Exception as e:
        #     raise SimpleException("Old password is not exists")
        #     print('e', e)
        # print("email", email)
        # if email in None:
        #     print('email error')
        #     raise "err"
        # user_info.active = True
        # user_info.update()
        # print(user_info)

    # def get_list_user(self):
    #     return self.dao.get_list_user()

    # def get_user_by_username(self, username):
    #     return self.dao.get_user_by_username(username)
