from src.services.base import BaseService
from utils.config import get_system_config
import hashlib
from src.models.message import Message
import boto3
import os
import time
from protos import upload_file_pb2


class UploadFileService(BaseService):
    def __init__(self):
        super().__init__(None)

    def upload_image(self, file_name, file_content, file_type, file_hash):
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3 and resize if needed
        tmp_file_name, file_ext = os.path.splitext(file_name)
        new_file_name = tmp_file_name + "_" +  str(round(time.time() * 1000)) + file_ext
        uploaded_file_url = self.upload_to_s3(new_file_name, file_content, file_type)
        obj_res = upload_file_pb2.UploadFilesResponse(
            file_url=uploaded_file_url
        )
        return obj_res

    def upload_file(self, file_name, file_content, file_type, file_hash):
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3
        tmp_file_name, file_ext = os.path.splitext(file_name)
        new_file_name = tmp_file_name + "_" +  str(round(time.time() * 1000)) + file_ext
        uploaded_file_url = self.upload_to_s3(new_file_name, file_content, file_type)

        obj_res = upload_file_pb2.UploadFilesResponse(
            file_url=uploaded_file_url
        )
        return obj_res

    def upload_chunked_file(self, request_iterator):
        data_blocks = []
        file_hash = None
        file_name = None
        file_content_type = None
        for request in request_iterator:
            m = hashlib.new('md5', request.file_data_block).hexdigest()
            if m != request.file_data_block_hash:
                raise Exception(Message.UPLOAD_FILE_DATA_LOSS)

            data_blocks.append(request.file_data_block)
            if not file_hash:
                file_hash = request.file_hash
                file_name = request.file_name
                file_content_type = request.file_content_type

        file_data = b''.join(data_blocks)
        m = hashlib.new('md5', file_data).hexdigest()
        if m != request.file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)

        # start upload to s3
        tmp_file_name, file_ext = os.path.splitext(file_name)
        new_file_name = tmp_file_name + "_" + str(round(time.time() * 1000)) + file_ext
        uploaded_file_url = self.upload_to_s3(new_file_name, file_data, file_content_type)

        obj_res = upload_file_pb2.UploadFilesResponse(
            file_url=uploaded_file_url
        )
        return obj_res

    def upload_to_s3(self, file_name, file_data, content_type):
        s3_config = get_system_config()['storage_s3']
        file_path = os.path.join(s3_config.get('folder'), file_name)
        s3_client = boto3.client('s3', aws_access_key_id=s3_config.get('access_key_id'), aws_secret_access_key=s3_config.get('access_key_secret'))
        s3_client.put_object(Body=file_data, Bucket=s3_config.get('bucket'), Key=file_path, ContentType=content_type, ACL='public-read')
        uploaded_file_url = os.path.join(s3_config.get('url'), s3_config.get('bucket'), file_path)
        print("Uploaded file url=", uploaded_file_url)
        return uploaded_file_url
