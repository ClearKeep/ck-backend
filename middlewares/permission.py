from functools import wraps
from utils.keycloak import KeyCloakUtils
import grpc
from utils.config import get_system_config
from msg.message import Message
import json


def auth_required(f):
    # @wraps(f)
    async def wrap(*args, **kwargs):
        context = args[2]
        metadata = dict(context.invocation_metadata())
        # client request with access_token
        if 'access_token' in metadata and _token_check(metadata['access_token']):
            return await f(*args, **kwargs)
        # server request with domain.
        if 'request_domain' in metadata and _fd_server_check(metadata['request_domain'], context.peer()):
            return await f(*args, **kwargs)
        # return error
        errors = [Message.get_error_object(Message.UNAUTHENTICATED)]
        context.set_details(json.dumps(errors, default=lambda x: x.__dict__))
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        return

    return wrap


def _token_check(access_token):
    try:
        token_info = KeyCloakUtils.introspect_token(access_token)
        print("permission.py => token info here=", token_info)
        if token_info['active']:
            return True
        else:
            return False
    except Exception as e:
        return False


def _fd_server_check(domain, ip_address):
    config = get_system_config()
    for item in config['fd_server']:
        if item['domain'] == domain and item['ip_address'] in ip_address:
            return True
    return False
