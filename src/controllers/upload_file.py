from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.upload_file import UploadFileService
import hashlib


class UploadFileController(BaseController):
    def __init__(self, *kwargs):
        self.service = UploadFileService()

    #@request_logged
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
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    #@request_logged
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
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
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
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.UPLOAD_FILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
