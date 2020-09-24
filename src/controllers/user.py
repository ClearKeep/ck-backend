import grpc
import proto.user_pb2_grpc as user_service
import proto.user_pb2 as user_messages

from src.controllers.base import *
from src.services.user import UserService
from utils.data import DataUtils
from utils.keycloak import KeyCloakUtils
from utils.encrypt import EncryptUtils

from middlewares.permission import *

class UserController(BaseController):
    def __init__(self, *kwargs):
        self.service = UserService()
    
    @auth_required
    def change_password(self, request, context):
        header_data = dict(context.invocation_metadata())
        introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
        self.service.change_password(request, request.old_password, request.new_password, introspect_token['sub'])
        return user_messages.SuccessResponse(success=True)

    @auth_required
    def get_user_info(self, request, context):
        header_data = dict(context.invocation_metadata())
        introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
        user_info = self.service.get_user_info(introspect_token['sub'], header_data['hash_key'])
        return user_messages.UserInfoResponse(
            id = user_info.id,
            username = user_info.username,
            email = user_info.email,
            first_name = user_info.first_name,
            last_name = user_info.last_name
        )

    def update_user_info(self, request, context):
        print('update_user_info', request)
        return user_messages.SuccessResponse(success=True)

    
