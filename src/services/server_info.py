from src.models.server_info import ServerInfo
from src.services.base import BaseService


class ServerInfoService(BaseService):
    def __init__(self):
        super().__init__(ServerInfo())

    def get_server_info(self):
        # get basic information about server, include stun_server and turn_server
        return ServerInfo().get()

    def update_server_info(self, stun_server, turn_server):
        # update basic information about server, include stun_server and turn_server
        self.model = ServerInfo(
            stun_server=stun_server,
            turn_server=turn_server
        )
        return self.model.update()
