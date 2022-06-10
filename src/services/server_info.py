from src.models.server_info import ServerInfo
from src.services.base import BaseService
from utils.config import get_system_config


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

    def get_stun(self):
        config = get_system_config()
        return {
            'server': f'stun:{config["server_domain"]}:{config["stun_turn_port"]}',
            'port': config["stun_turn_port"]
        }

    def get_turn(self):
        config = get_system_config()
        return {
            "server": f'turn:{config["server_domain"]}:{config["stun_turn_port"]}',
            "port": config["stun_turn_port"],
            "type": "udp",
            "user": config["stun_turn_credential"]["coturn_user"],
            "pwd": config["stun_turn_credential"]["coturn_password"]
        }
