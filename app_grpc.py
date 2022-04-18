import os
from utils.logger import *
import grpc
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
import protos.upload_file_pb2_grpc as upload_file_service
import protos.workspace_pb2_grpc as workspace_service
import protos.note_pb2_grpc as note_service
from src.controllers.user import UserController
from src.controllers.auth import AuthController
from src.controllers.signal import SignalController
from src.controllers.group import GroupController
from src.controllers.message import MessageController
from src.controllers.notify_inapp import NotifyInAppController
from src.controllers.notify_push import NotifyPushController
from src.controllers.video_call import VideoCallController
from src.controllers.server_info import ServerInfoController
from src.controllers.upload_file import UploadFileController
from src.controllers.workspace import WorkspaceController
from src.controllers.note import NoteController
# from middlewares.auth_interceptor import AuthInterceptor
import asyncio
from grpc import aio
from utils.keycloak import KeyCloakUtils


async def start_server():
    grpc_port = get_system_config()['grpc_port']
    server = grpc.aio.server()
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(AuthInterceptor(),))
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    user_service.add_UserServicer_to_server(UserController(), server)
    auth_service.add_AuthServicer_to_server(AuthController(), server)
    signal_service.add_SignalKeyDistributionServicer_to_server(SignalController(), server)
    group_service.add_GroupServicer_to_server(GroupController(), server)
    message_service.add_MessageServicer_to_server(MessageController(), server)
    notify_inapp_service.add_NotifyServicer_to_server(NotifyInAppController(), server)
    notify_push_service.add_NotifyPushServicer_to_server(NotifyPushController(), server)
    video_call_service.add_VideoCallServicer_to_server(VideoCallController(), server)
    server_info_service.add_ServerInfoServicer_to_server(ServerInfoController(), server)
    upload_file_service.add_UploadFileServicer_to_server(UploadFileController(), server)
    workspace_service.add_WorkspaceServicer_to_server(WorkspaceController(), server)
    note_service.add_NoteServicer_to_server(NoteController(), server)
    # init log
    os.makedirs("logs", exist_ok=True)
    create_timed_rotating_log('logs/logfile-' + str(grpc_port) + '.log')
    # start grpc api
    grpc_add = "0.0.0.0:{}".format(grpc_port)
    server.add_insecure_port(grpc_add)
    await server.start()
    print("gRPC listening on port {}..".format(grpc_port))
    logger.info("gRPC listening on port {}..".format(grpc_port))

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)


if __name__ == '__main__':
    asyncio.run(start_server())
