from src.services.base import BaseService
from utils.config import get_system_config
import hashlib
from src.models.message import Message
import boto3
from botocore.exceptions import ClientError
import os
import time
from protos import upload_file_pb2


class UploadFileService(BaseService):
    """
    Upload file service, for upload image/file to server
    """
    def __init__(self):
        super().__init__(None)

    def get_upload_file_link(self, file_name, file_type, uploader, access_control_list='private', expiration=3600):
        # get pre presigned url for directly upload file
        s3_config = get_system_config()['storage_s3']
        file_path = os.path.join(s3_config.get('folder'), uploader, str(round(time.time()*100)), file_name)
        s3_client = boto3.client('s3', aws_access_key_id=s3_config.get('access_key_id'),
                                 aws_secret_access_key=s3_config.get('access_key_secret'))
        url_response = s3_client.generate_presigned_url('put_object',
                                                        Params={'Bucket': s3_config.get('bucket'),
                                                                'Key': file_path,
                                                                'ContentType': file_type,
                                                                'ACL': access_control_list
                                                            },
                                                        ExpiresIn=expiration
                                                        )
        if access_control_list in ['public-read', 'public-read-write']:
            file_url = os.path.join(s3_config.get('url'), s3_config.get('bucket'), file_path)
        else:
            file_url = ""
        return upload_file_pb2.GetUploadFileLinkResponse(
                uploaded_file_url=url_response,
                download_file_url=file_url,
                object_file_path=file_path
        )

    def get_download_file_link(self, file_path, downloader, expiration=3600):
        # get pre presigned url for directly download file
        assert downloader != "" # verify reading access of downloader
        s3_config = get_system_config()['storage_s3']
        s3_client = boto3.client('s3', aws_access_key_id=s3_config.get('access_key_id'),
                                 aws_secret_access_key=s3_config.get('access_key_secret'))
        url_response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': s3_config.get('bucket'),
                                                                'Key': file_path},
                                                        ExpiresIn=expiration)
        return upload_file_pb2.GetDownloadFileLinkResponse(
                download_file_url=url_response
        )

    def upload_image(self, file_name, file_content, file_type, file_hash):
        # upload an image with remained info, then return a downloaded link
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3 and resize if needed
        tmp_file_name, file_ext = os.path.splitext(file_name)
        new_file_name = tmp_file_name + "_" + str(round(time.time() * 1000)) + file_ext
        uploaded_file_url = self.upload_to_s3(new_file_name, file_content, file_type)
        obj_res = upload_file_pb2.UploadFilesResponse(
            file_url=uploaded_file_url
        )
        return obj_res

    def upload_file(self, file_name, file_content, file_type, file_hash):
        # upload a file_content with remained info, then return a downloaded link
        m = hashlib.new('md5', file_content).hexdigest()
        if m != file_hash:
            raise Exception(Message.UPLOAD_FILE_DATA_LOSS)
        # start upload to s3
        tmp_file_name, file_ext = os.path.splitext(file_name)
        new_file_name = tmp_file_name + "_" + str(round(time.time() * 1000)) + file_ext
        uploaded_file_url = self.upload_to_s3(new_file_name, file_content, file_type)

        obj_res = upload_file_pb2.UploadFilesResponse(
            file_url=uploaded_file_url
        )
        return obj_res

    async def upload_chunked_file(self, request_iterator):
        # upload a chunked_file, useful when upload large file
        data_blocks = []
        file_hash = None
        file_name = None
        file_content_type = None

        async for request in request_iterator:
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
        # s3 uploader
        s3_config = get_system_config()['storage_s3']
        file_path = os.path.join(s3_config.get('folder'), file_name)
        s3_client = boto3.client('s3', aws_access_key_id=s3_config.get('access_key_id'),
                                 aws_secret_access_key=s3_config.get('access_key_secret'))
        s3_client.put_object(Body=file_data, Bucket=s3_config.get('bucket'), Key=file_path, ContentType=content_type,
                             ACL='public-read')
        uploaded_file_url = os.path.join(s3_config.get('url'), s3_config.get('bucket'), file_path)
        return uploaded_file_url
