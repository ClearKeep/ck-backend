from aiohttp import web
import json
from src.services.server_info import ServerInfoService


class Server():
    def get(self):
        server_info = ServerInfoService().get_server_info()
        turn_server = json.loads(server_info.turn_server)
        uri = "turn:{}:{}?transport={}"
        response = {
            "username": turn_server.get('user'),
            "password": turn_server.get('pwd'),
            "ttl": 86400,
            "uris": [
                uri.format(turn_server.get("server"), turn_server.get("port"), turn_server.get("type"))
            ]
        }
        return response
