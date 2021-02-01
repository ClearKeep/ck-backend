# Retrieve a Network Traversal Service Token
from twilio.rest import Client
import os
import json
from protos import server_info_pb2, server_info_pb2_grpc
import grpc
from utils.logger import *
from utils.config import get_system_config

# env = os.getenv("ENV")
# env_name = env if env else 'development'
# with open(f'./configs/{env_name}.json') as json_data_file:
#     data = json.load(json_data_file)
# print("Load config env=", env_name)

def generate_stun_turn_credential():
    data = get_system_config()
    account_sid = data['stun_turn_credential'].get('twilio_account_sid')
    auth_token = data['stun_turn_credential'].get('twilio_auth_token')
    client = Client(account_sid, auth_token)
    token = client.tokens.create()
    #
    stun_obj = token.ice_servers[0]
    stun_url = stun_obj["url"]
    #
    stun = {
        "server": stun_url,
        "port": 3478
    }
    str_stun = json.dumps(stun)
    print("str_stun=", str_stun)

    turn_obj = token.ice_servers[1]
    turn = {
        "server": turn_obj["url"],
        "port": 3478,
        "type": "udp",
        "user": turn_obj["username"],
        "pwd": turn_obj["credential"]
    }
    str_turn = json.dumps(turn)
    print("str_turn=", str_turn)

    return str_stun, str_turn


def update_stun_turn_credential():
    try:
        stun, turn = generate_stun_turn_credential()
        host = "localhost"  # data['']
        port = 5000  # data['']
        channel = grpc.insecure_channel(host + ':' + str(port))
        stub = server_info_pb2_grpc.ServerInfoStub(channel)

        request = server_info_pb2.UpdateNTSReq(stun=stun, turn=turn)
        response = stub.update_nts(request)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    update_stun_turn_credential()
