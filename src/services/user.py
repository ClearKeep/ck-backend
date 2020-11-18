from src.services.base import BaseService
from src.models.user import User
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils
from proto import user_pb2


class UserService(BaseService):
    def __init__(self):
        super().__init__(User())

    def create_new_user(self, id, record, auth_source):
        self.model = User(
            id=id,
            username=record.username,
            auth_source=auth_source
        )
        if record.email:
            self.model.email = EncryptUtils.encrypt_data(record.email, record.password, id)
        if record.first_name:
            self.model.first_name = EncryptUtils.encrypt_data(record.first_name, record.password, id)
        if record.last_name:
            self.model.last_name = EncryptUtils.encrypt_data(record.last_name, record.password, id)

        return self.model.add()

    def change_password(self, request, old_pass, new_pass, user_id):
        user_info = self.find_by_id(user_id)

        response = KeyCloakUtils.set_user_password(user_id, new_pass)

        if user_info.email:
            email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
            user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
        if user_info.first_name:
            first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
            user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
        if user_info.last_name:
            last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)
            user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)

        return user_info.update()

    def get_profile(self, user_id, hash_key):
        user_info = self.find_by_id(user_id)
        if user_info is not None:
            obj_res = user_pb2.UserProfileResponse(
                id=user_info.id,
                username=user_info.username,
                # email=EncryptUtils.decrypt_with_hash(user_info.email, hash_key),
                # first_name=EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key),
                # last_name=EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key)
            )
            if user_info.email:
                obj_res.email = EncryptUtils.decrypt_with_hash(user_info.email, hash_key)
            if user_info.first_name:
                obj_res.first_name = EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key),
            if user_info.last_name:
                obj_res.last_name = EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key),

            return obj_res
        else:
            return None

    def update_profile(self, request, user_id, hash_key):
        user_info = self.find_by_id(user_id)
        if request.username:
            user_info.username = request.username

        if request.email:
            user_info.email = EncryptUtils.encrypt_with_hash(request.email, hash_key)

        if request.first_name:
            user_info.first_name = EncryptUtils.encrypt_with_hash(request.first_name, hash_key)

        if request.last_name:
            user_info.last_name = EncryptUtils.encrypt_with_hash(request.last_name, hash_key)

        return user_info.update()

    def get_user_info(self, client_id):
        user_info = self.find_by_id(client_id)
        if user_info is not None:
            return user_pb2.UserInfoResponse(
                id=user_info.id,
                username=user_info.username
            )
        else:
            return None

    def search_user(self, keyword):
        lst_user = self.model.search(keyword)
        lst_obj_res = []
        for obj in lst_user:
            obj_res = user_pb2.UserInfoResponse(
                id=obj.id,
                username=obj.username,
            )
            lst_obj_res.append(obj_res)

        response = user_pb2.SearchUserResponse(
            lst_user=lst_obj_res
        )
        return response

    def get_users(self, client_id):
        lst_user = self.model.get_users(client_id)
        lst_obj_res = []
        for obj in lst_user:
            obj_res = user_pb2.UserInfoResponse(
                id=obj.id,
                username=obj.username,
            )
            lst_obj_res.append(obj_res)

        response = user_pb2.GetUsersResponse(
            lst_user=lst_obj_res
        )
        return response
