# Retrieve a Network Traversal Service Token
from protos import upload_file_pb2, upload_file_pb2_grpc
import grpc
from utils.logger import *
from utils.config import get_system_config
import hashlib

filename = "./client-test/upload_file/photo.png"


def upload_photo():
    try:
        with open(filename, mode='rb') as file:
            file_data = file.read()
            content_type = "image/png"
            hash = hashlib.new('md5', file_data).hexdigest()

            data = get_system_config()
            host = data['server_domain']
            port = data['grpc_port']

            # update for production branch
            channel = grpc.insecure_channel('localhost:25000')
            stub = upload_file_pb2_grpc.UploadFileStub(channel)
            request = upload_file_pb2.FileUploadRequest(file_name="photo.png", file_content_type=content_type,
                                                        file_data=file_data, file_hash=hash)
            stub.upload_image(request)
            print('Set cronjob succesful')

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    upload_photo()
