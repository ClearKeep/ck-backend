from src.services.base import BaseService
from src.models.user import User
from utils.encrypt import EncryptUtils
from utils.keycloak import KeyCloakUtils
from protos import user_pb2
from utils.config import get_system_domain
from utils.logger import *
from msg.message import Message
import datetime


class UserService(BaseService):
    def __init__(self):
        super().__init__(User())
        #self.domain = get_system_domain()

    def create_new_user(self, id, email, display_name, auth_source):
        # password, first_name, last_name,
        try:
            self.model = User(
                id=id,
                email=email,
                display_name=display_name,
                auth_source=auth_source
            )
            # if email:
            #     self.model.email = EncryptUtils.encrypt_data(email, password, id)
            # if first_name:
            #     self.model.first_name = EncryptUtils.encrypt_data(first_name, password, id)
            # if last_name:
            #     self.model.last_name = EncryptUtils.encrypt_data(last_name, password, id)
            self.model.add()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def create_user_social(self, id, email, display_name, auth_source):
        try:
            self.model = User(
                id=id,
                email=email,
                display_name=display_name,
                auth_source=auth_source,
                last_login_at=datetime.datetime.now()
            )
            # if email:
            #     self.model.email = EncryptUtils.encrypt_data(email, password, id)
            # if first_name:
            #     self.model.first_name = EncryptUtils.encrypt_data(first_name, password, id)
            # if last_name:
            #     self.model.last_name = EncryptUtils.encrypt_data(last_name, password, id)
            self.model.add()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.REGISTER_USER_FAILED)

    def get_google_user(self, email, auth_source):
        user_info = self.model.get_google_user(email, auth_source)
        return user_info


    def change_password(self, request, old_pass, new_pass, user_id):
        try:
            user_info = self.model.get(user_id)
            response = KeyCloakUtils.set_user_password(user_id, new_pass)
            # if user_info.email:
            #     email = EncryptUtils.decrypt_data(user_info.email, old_pass, user_id)
            #     user_info.email = EncryptUtils.encrypt_data(email, new_pass, user_id)
            # if user_info.first_name:
            #     first_name = EncryptUtils.decrypt_data(user_info.first_name, old_pass, user_id)
            #     user_info.first_name = EncryptUtils.encrypt_data(first_name, new_pass, user_id)
            # if user_info.last_name:
            #     last_name = EncryptUtils.decrypt_data(user_info.last_name, old_pass, user_id)
            #     user_info.last_name = EncryptUtils.encrypt_data(last_name, new_pass, user_id)

            return user_info.update()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.CHANGE_PASSWORD_FAILED)

    def get_profile(self, user_id, hash_key):
        try:
            user_info = self.model.get(user_id)
            if user_info is not None:
                obj_res = user_pb2.UserProfileResponse(
                    id=user_info.id,
                    display_name=user_info.display_name
                )
                if user_info.email:
                    obj_res.email = user_info.email
                # if user_info.first_name:
                #     obj_res.first_name = EncryptUtils.decrypt_with_hash(user_info.first_name, hash_key),
                # if user_info.last_name:
                #     obj_res.last_name = EncryptUtils.decrypt_with_hash(user_info.last_name, hash_key),

                return obj_res
            else:
                return None
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_PROFILE_FAILED)

    def update_profile(self, request, user_id, hash_key):
        try:
            user_info = self.model.get(user_id)
            if request.display_name:
                user_info.display_name = request.display_name

            # if request.email:
            #     user_info.email = EncryptUtils.encrypt_with_hash(request.email, hash_key)
            # if request.first_name:
            #     user_info.first_name = EncryptUtils.encrypt_with_hash(request.first_name, hash_key)
            #
            # if request.last_name:
            #     user_info.last_name = EncryptUtils.encrypt_with_hash(request.last_name, hash_key)

            return user_info.update()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.UPDATE_PROFILE_FAILED)

    def get_user_info(self, client_id, workspace_domain):
        try:
            user_info = self.model.get(client_id)
            if user_info is not None:
                return user_pb2.UserInfoResponse(
                    id=user_info.id,
                    display_name=user_info.display_name,
                    workspace_domain=workspace_domain
                )
            else:
                raise Exception(Message.GET_USER_INFO_FAILED)
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_USER_INFO_FAILED)

    def search_user(self, keyword, client_id):
        try:
            lst_user = self.model.search(keyword, client_id)
            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj.id,
                    display_name=obj.display_name,
                )
                lst_obj_res.append(obj_res)

            response = user_pb2.SearchUserResponse(
                lst_user=lst_obj_res
            )
            return response
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.SEARCH_USER_FAILED)

    def get_users(self, client_id, workspace_domain):
        try:
            lst_user = self.model.get_users(client_id)
            lst_obj_res = []
            for obj in lst_user:
                obj_res = user_pb2.UserInfoResponse(
                    id=obj.id,
                    display_name=obj.display_name,
                    workspace_domain=workspace_domain,
                )
                lst_obj_res.append(obj_res)

            response = user_pb2.GetUsersResponse(
                lst_user=lst_obj_res
            )
            return response
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
            raise Exception(Message.GET_USER_INFO_FAILED)

    def update_last_login(self, user_id):
        try:
            user_info = self.model.get(user_id)
            user_info.last_login_at = datetime.datetime.now()
            user_info.update()
        except Exception as e:
            logger.info(bytes(str(e), encoding='utf-8'))
