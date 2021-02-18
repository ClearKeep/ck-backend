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
from src.controllers import app
from crontab import CronTab
import os


def start_server():
    grpc_port = get_system_config()['grpc_port']
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

    # start grpc api
    grpc_add = "0.0.0.0:{}".format(grpc_port)
    server.add_insecure_port(grpc_add)
    server.start()
    print("gRPC listening on port {}..".format(grpc_port))
    logger.info("gRPC listening on port {}..".format(grpc_port))

    # set cronjob
    cron_tab_update_turn_server()
    # log total thread
    #get_thread()

    # start http api
    http_port = get_system_config()['http_port']
    print("HTTP listening on port {}..".format(http_port))
    logger.info("HTTP listening on port {}..".format(http_port))
    app.run(host="0.0.0.0", port=str(http_port), threaded=False, processes=3, debug=False)

    server.wait_for_termination()



def get_thread():
    total = threading.activeCount()
    logger.info("Total thread= {}".format(total))
    time.sleep(1800)
    get_thread()


def cron_tab_update_turn_server():
    try:
        # run in the first time
        os.system('ENV=stagging python3 -m client.client_nts')
        # set cronjob in next time
        cron = CronTab(user='ubuntu')
        cron.remove_all()
        job = cron.new(command='ENV=stagging python3 -m client.client_nts')
        job.hour.on(1)
        cron.write()
        logger.info("Cronjob cron_tab_update_turn_server set")

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    start_server()
