from src.services.base import BaseService
from protos import upload_file_pb2
from utils.config import get_system_config
import requests
import json
import secrets
import datetime
import hashlib
from src.models.message import Message


class UploadFileService(BaseService):
    def __init__(self):
        super().__init__(None)

    def upload_image(self, file_content, file_type, file_hash):
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3 and resize if needed

    def upload_file(self, file_content, file_type, file_hash):
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3

    def upload_chunked_file(self, request_iterator):
        data_blocks = []
        file_hash = None
        file_name = None
        for request in request_iterator:
            m = hashlib.new('md5', request.file_data_block).hexdigest()
            if m != request.file_data_block_hash:
                raise Exception(Message.UPLOAD_FILE_DATA_LOSS)

            data_blocks.append(request.file_data_block)
            if not file_hash:
                file_hash = request.file_hash
                file_name = request.file_name

        file_data = b''.join(data_blocks)
        m = hashlib.new('md5', file_data).hexdigest()
        if m != request.file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)

        # start upload to s3

