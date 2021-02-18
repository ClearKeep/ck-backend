import asyncio
import os
import threading

import grpc
from aiohttp import web
from crontab import CronTab
from grpc.experimental.aio import init_grpc_aio

import protos.auth_pb2_grpc as auth_service
import protos.group_pb2_grpc as group_service
import protos.message_pb2_grpc as message_service
import protos.notify_pb2_grpc as notify_inapp_service
import protos.notify_push_pb2_grpc as notify_push_service
import protos.server_info_pb2_grpc as server_info_service
import protos.signal_pb2_grpc as signal_service
import protos.user_pb2_grpc as user_service
import protos.video_call_pb2_grpc as video_call_service
from src.controllers.auth import AuthController
from src.controllers.group import GroupController
from src.controllers.message import MessageController
from src.controllers.notify_inapp import NotifyInAppController
from src.controllers.notify_push import NotifyPushController
from src.controllers.server_info import ServerInfoController
from src.controllers.signal import SignalController
from src.controllers.turn_server import Server
from src.controllers.user import UserController
from src.controllers.video_call import VideoCallController
from src.models.base import db
from utils.config import get_system_config
from utils.logger import *


def get_thread():
    total = threading.activeCount()
    logger.info("Total thread= {}".format(total))
    time.sleep(100)
    get_thread()


def cron_tab_update_turn_server():
    try:
        # run in the first time
        os.system('ENV=stagging python3 -m client.client_nts')
        # set cronjob in next time
        cron = CronTab(user='ubuntu')
        cron.remove_all()
        job = cron.new(command='ENV=stagging python3 -m client.client_nts')
        # job.hour.on(1)
        job.minute.every(30)
        cron.write()
        logger.info("Cronjob cron_tab_update_turn_server set")

    except Exception as e:
        logger.error(e)

class Server_info(web.View):
    async def get(self):
        response = {
            "thread_count": threading.activeCount(),
        }
        return web.json_response(response)

class GrpcServer:
    def __init__(self):
        init_grpc_aio()
        grpc_port = get_system_config()['grpc_port']
        self.server = grpc.experimental.aio.server()
        self.authController = AuthController()
        self.userController = UserController()
        self.signalController = SignalController()
        self.groupController = GroupController()
        self.messageController = MessageController()
        self.notifyInAppController = NotifyInAppController()
        self.notifyPushController = NotifyPushController()
        self.videoCallController = VideoCallController()
        self.serverInfoController = ServerInfoController()
        user_service.add_UserServicer_to_server(self.userController, self.server)
        auth_service.add_AuthServicer_to_server(self.authController, self.server)
        signal_service.add_SignalKeyDistributionServicer_to_server(self.signalController, self.server)
        group_service.add_GroupServicer_to_server(self.groupController, self.server)
        message_service.add_MessageServicer_to_server(self.messageController, self.server)
        notify_inapp_service.add_NotifyServicer_to_server(self.notifyInAppController, self.server)
        notify_push_service.add_NotifyPushServicer_to_server(self.notifyPushController, self.server)
        video_call_service.add_VideoCallServicer_to_server(self.videoCallController, self.server)
        server_info_service.add_ServerInfoServicer_to_server(self.serverInfoController, self.server)

        grpc_add = "0.0.0.0:{}".format(grpc_port)
        self.server.add_insecure_port(grpc_add)
        print("gRPC listening on port {}..".format(grpc_port))
        logger.info("gRPC listening on port {}..".format(grpc_port))

    async def start(self):
        await self.server.start()
        await self.server.wait_for_termination()

    async def stop(self):
        await self.authController.close()
        await self.userController.close()
        await self.signalController.close()
        await self.groupController.close()
        await self.messageController.close()
        await self.notifyInAppController.close()
        await self.notifyPushController.close()
        await self.videoCallController.close()
        await self.serverInfoController.close()
        await self.server.wait_for_termination()


class Application(web.Application):
    def __init__(self):
        super().__init__()
        self.grpc_task = None
        self.grpc_server = GrpcServer()
        self.add_routes()
        self.init_all()
        self.on_startup.append(self.__on_startup())
        self.on_shutdown.append(self.__on_shutdown())

    def __on_startup(self):
        async def _on_startup(app):
            self.grpc_task = \
                asyncio.ensure_future(app.grpc_server.start())

        return _on_startup

    def __on_shutdown(self):
        async def _on_shutdown(app):
            await app.grpc_server.stop()
            app.grpc_task.cancel()
            await app.grpc_task

        return _on_shutdown

    def add_routes(self):
        self.router.add_view('/turn-server', Server)
        self.router.add_view('/server-info', Server_info)

    def init_all(self):
        # create all table in database
        db.create_all()
        # init log
        create_timed_rotating_log('logs/logfile.log')

        # set cronjob
        cron_tab_update_turn_server()

    def run(self):
        # start http api
        http_port = get_system_config()['http_port']
        web.run_app(self, port=int(http_port))


application = Application()

if __name__ == '__main__':
    application.run()
