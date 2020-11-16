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
            email=EncryptUtils.encrypt_data(record.email, record.password, id),
            username=record.username,
            first_name=EncryptUtils.encrypt_data(record.first_name, record.password, id),
            last_name=EncryptUtils.encrypt_data(record.last_name, record.password, id),
            auth_source=auth_source
        )
        return self.model.add()

    def change_password(self, request, old_pass, new_pass, user_id):
        user_info = self.find_by_id(user_id)

        response = KeyCloakUtils.set_user_password(user_id, new_pass)

        email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
        first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
        last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)

        user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
        user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
        user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)

        return user_info.update()

    def get_profile(self, user_id, hash_key):
        user_info = self.find_by_id(user_id)
        if user_info is not None:
            obj_res = user_pb2.UserProfileResponse(
                id=user_info.id,
                username=user_info.username,
                email=EncryptUtils.decrypt_with_hash(user_info.email, hash_key),
                # first_name=EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key),
                # last_name=EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key)
            )
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
