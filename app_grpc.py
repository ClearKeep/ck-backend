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
    # init log
    create_timed_rotating_log('logs/logfile.log')

    # KeyCloakUtils.create_user_with_email(email="phuong.nguyen@vmodev.com")
    # token = KeyCloakUtils.introspect_token("eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJOTjdvRERUY1B1aWx0eU41OWhQWkJQUWlaT1VHajZyUUxPa0dPSjRyalRnIn0.eyJleHAiOjE2MTcwOTMyNjYsImlhdCI6MTYxNzA4OTY2NiwianRpIjoiYjVhMDJlMzYtNmNhZi00YjFiLTlhM2QtZjBlMjhmNzYzZDY1IiwiaXNzIjoiaHR0cDovLzU0LjIzNS42OC4xNjA6MjgwODAvYXV0aC9yZWFsbXMvbWFzdGVyIiwic3ViIjoiODU4MDY4NmQtMjBlNS00OTc3LTg4MTMtODI3OThlY2Q0ZDZhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYWRtaW4tY2xpIiwic2Vzc2lvbl9zdGF0ZSI6IjIwMjY2YmNkLTNmZTgtNDkzZC1hMDQ2LWM2OTdlNTgxMzc5MSIsImFjciI6IjEiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InBodW9uZy5uZ3V5ZW5Adm1vZGV2LmNvbSIsImdpdmVuX25hbWUiOiIiLCJmYW1pbHlfbmFtZSI6IiIsImVtYWlsIjoicGh1b25nLm5ndXllbkB2bW9kZXYuY29tIn0.Nh_-ynIrhcYalpEG9A6A0OYFNMJUEv06xBj0u14rMu3HqmBgs5pbWvpHvQuriovYv9FsUYgqkcyoQa8257sD9XsokNPX9K2Iy8WicSTaIiqIC4S00JwRHgwNGKU8yJF9qV0qPFnFk7IaRVy1ttQYaZAFCWD2jwDnejfOLpZ6H7CH_884JjxsVRtaulERKOeXiIR_H5QTDc4GrTv5kAu0BQItE7tWwvrPK2htJUGgwJMktTGfE8zEUY0XbvJ36QPvTqSzwlhOyFAclAInVjlZstSUI9kwMhnH8HTRPwyj-vcfWTyTjoG0HOZDgJpTJW1SPyKF1ZqMLJru0n1EUbKrzQ")
    # token = KeyCloakUtils.exchange_token("8580686d-20e5-4977-8813-82798ecd4d6a")
    # access_token = KeyCloakUtils.introspect_token(token["access_token"])

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
