# Retrieve a Network Traversal Service Token
from twilio.rest import Client
from utils.config import get_system_config
from src.services.server_info import ServerInfoService

account_sid = get_system_config()['stun_turn_credential'].get('twilio_account_sid')
auth_token = get_system_config()['stun_turn_credential'].get('twilio_auth_token')
client = Client(account_sid, auth_token)
token = client.tokens.create()

server_info = ServerInfoService().update_server_info("stun", "turn")

