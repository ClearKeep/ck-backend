from src.models.server_info import ServerInfo
from src.services.base import BaseService

class ServerInfoService(BaseService):
    def __init__(self):
        super().__init__(ServerInfo())

    def get_server_info(self):
        return ServerInfo().get()