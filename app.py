from concurrent import futures
import grpc
from src.models.base import db
from utils.config import get_system_config
import protos.user_pb2_grpc as user_service
import protos.auth_pb2_grpc as auth_service
import protos.signal_pb2_grpc as signal_service
import protos.group_pb2_grpc as group_service
import protos.message_pb2_grpc as message_service
import protos.notify_pb2_grpc as notify_inapp_service
import protos.notify_push_pb2_grpc as notify_push_service
import protos.video_call_pb2_grpc as video_call_service
import protos.server_info_pb2_grpc as server_info_service
from src.controllers.user import UserController
from src.controllers.auth import AuthController
from src.controllers.signal import SignalController
from src.controllers.group import GroupController
from src.controllers.message import MessageController
from src.controllers.notify_inapp import NotifyInAppController
from src.controllers.notify_push import NotifyPushController
from src.controllers.video_call import VideoCallController
from src.controllers.server_info import ServerInfoController
from utils.logger import *
# from middlewares.auth_interceptor import AuthInterceptor
import threading
import time

def grpc_server(port):
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(AuthInterceptor(),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    user_service.add_UserServicer_to_server(UserController(), server)
    auth_service.add_AuthServicer_to_server(AuthController(), server)
    signal_service.add_SignalKeyDistributionServicer_to_server(SignalController(), server)
    group_service.add_GroupServicer_to_server(GroupController(), server)
    message_service.add_MessageServicer_to_server(MessageController(), server)
    notify_inapp_service.add_NotifyServicer_to_server(NotifyInAppController(), server)
    notify_push_service.add_NotifyPushServicer_to_server(NotifyPushController(), server)
    video_call_service.add_VideoCallServicer_to_server(VideoCallController(), server)
    server_info_service.add_ServerInfoServicer_to_server(ServerInfoController(), server)
    # create all table in database
    db.create_all()
    # init log
    create_timed_rotating_log('logs/logfile.log')

    # init_firebase_app()

    server.add_insecure_port('0.0.0.0:5000')
    server.start()

    print("Listening on port {}..".format(port))
    logger.info("Listening on port {}..".format(port))

    get_thread()

    server.wait_for_termination()

def get_thread():
    total = threading.activeCount()
    logger.info("Total thread= {}".format(total))
    time.sleep(3600)
    get_thread()


if __name__ == '__main__':
    port = get_system_config()['port']
    grpc_server(port)
