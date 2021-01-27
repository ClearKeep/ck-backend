from src.models.server_info import Server_info
from src.services.base import BaseService

class ServerService(BaseService):
    def __init__(self):
        super().__init__(Server_info())

    def get_info(self):
        return Server_info().get_info()