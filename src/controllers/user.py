import grpc
import proto.user_pb2_grpc as user_service
import proto.user_pb2 as user_messages

from src.controllers.base import *
from src.services.user import UserService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils
from utils.encrypt import EncryptUtils

class UserController(BaseController):
    def __init__(self, *kwargs):
        self.service = UserService()

    def get_user(self, request, context):
        username = request.username
        found = self.service.get_user_by_username(username)
        # token = KeyCloakUtils.getToken('tulp', '123456')
        # print(token)
        if found:
            return user_messages.UserResponse(**DataUtils.object_as_dict(found))

        context.set_details('user is not found')
        context.set_code(grpc.StatusCode.NOT_FOUND)

        return user_messages.UserResponse()

    @auth_required
    def get_list_user(self, request, context):

        found = self.service.get_list_user()
        data = list(map(lambda item: user_messages.UserResponse(**DataUtils.object_as_dict(item)), found))
        # data = list(map(lambda item: user_messages.UserResponse(id=item.id, username=item.username, email=item.email), found))
        return user_messages.UsersResponseList(list=data)

    def change_password(self, request, context):
        token = dict(context.invocation_metadata())
        introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
        print('asdasdasd', introspect_token)
        # self.service.change_password()
        self.service.change_password(request, request.old_password, request.new_password, introspect_token['sub'])
        # user_info = self.service.find_by_id(introspect_token['sub'])
        # try:
        #     email = EncryptUtils.decrypt_data(user_info.email, request.old_password, introspect_token['sub'])
        # except Exception as e:
        #     print(e)
        # print(email)

        # print(request)
