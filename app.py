from concurrent import futures
import grpc
from src.models.base import db
from utils.config import get_system_config
import proto.user_pb2_grpc as user_service
import proto.auth_pb2_grpc as auth_service
import proto.signal_pb2_grpc as signal_service
from src.controllers.user import UserController
from src.controllers.auth import AuthController
from src.controllers.signal import SignalController

from utils.logger import *
#from middlewares.auth_interceptor import AuthInterceptor

def grpc_server(port):

    #server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(AuthInterceptor(),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service.add_UserServicer_to_server(UserController(), server)
    auth_service.add_AuthServicer_to_server(AuthController(), server)
    signal_service.add_SignalKeyDistributionServicer_to_server(SignalController(), server)

    # create all table in database
    db.create_all()
    # init log
    create_timed_rotating_log('logs/logfile.log')

    server.add_insecure_port('0.0.0.0:5000')
    server.start()

    print("Listening on port {}..".format(port))
    logger.info("Listening on port {}..".format(port))

    server.wait_for_termination()


if __name__ == '__main__':
    port = get_system_config()['port']
    grpc_server(port)
