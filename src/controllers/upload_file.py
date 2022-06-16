from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.upload_file import UploadFileService
import hashlib

import logging
logger = logging.getLogger(__name__)
class UploadFileController(BaseController):
    def __init__(self, *kwargs):
        self.service = UploadFileService()

    @request_logged
    async def upload_image(self, request, context):
        try:
            file_name = request.file_name
            file_data = request.file_data
            file_content_type = request.file_content_type
            file_hash = request.file_hash
            obj_res = self.service.upload_image(file_name, file_data, file_content_type, file_hash)

            return obj_res

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def upload_file(self, request, context):
        try:
            file_name = request.file_name
            file_content = request.file_data
            file_content_type = request.file_content_type
            file_hash = request.file_hash
            obj_res = self.service.upload_file(file_name, file_content, file_content_type, file_hash)
            return obj_res

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    #@request_logged
    async def upload_chunked_file(self, request_iterator, context):
        try:
            obj_res = await self.service.upload_chunked_file(request_iterator)
            return obj_res

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def get_upload_file_link(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            access_control_list = 'public-read' if request.is_public else "private"
            obj_res = self.service.get_upload_file_link(request.file_name, request.file_content_type, client_id, access_control_list=access_control_list)
            return obj_res

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def get_download_file_link(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            obj_res = self.service.get_download_file_link(request.object_file_path, client_id)
            return obj_res
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
