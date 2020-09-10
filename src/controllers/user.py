import grpc
import proto.user_pb2_grpc as user_service
import proto.user_pb2 as user_messages

from src.controllers.base import *
from src.services.user import UserService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils

class UserController(BaseController):
    def __init__(self, *kwargs):
        self.service = UserService()

    def GetUser(self, request, context):
        username = request.username
        found = self.service.getUserByUsername(username)
        # token = KeyCloakUtils.getToken('tulp', '123456')
        # print(token)
        if found:
            return user_messages.UserResponse(**DataUtils.object_as_dict(found))

        context.set_details('user is not found')
        context.set_code(grpc.StatusCode.NOT_FOUND)

        return user_messages.UserResponse()

    @auth_required
    def GetUsers(self, request, context):

        found = self.service.getListUser()
        data = list(map(lambda item: user_messages.UserResponse(**DataUtils.object_as_dict(item)), found))
        # data = list(map(lambda item: user_messages.UserResponse(id=item.id, username=item.username, email=item.email), found))
        return user_messages.UsersResponseList(list=data)
