from functools import wraps
from utils.keycloak import KeyCloakUtils
import grpc
from utils.config import get_system_config
from msg.message import Message
import json
from utils.logger import *


def auth_required(f):
    # @wraps(f)
    async def wrap(*args, **kwargs):
        context = args[2]
        metadata = dict(context.invocation_metadata())
        # client request with access_token
        if 'access_token' in metadata:
            if _token_check(metadata['access_token']):
                return await f(*args, **kwargs)
            else:
                errors = [Message.get_error_object(Message.INVALID_ACCESS_TOKEN)]
                context.set_details(json.dumps(errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.INTERNAL)
                return
        return await f(*args, **kwargs)
        # server request with domain.

        logger.info('peer context: ' + context.peer())
        if _fd_server_check(context.peer()):
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
        logger.info({"token info": token_info})
        if token_info['active']:
            return True
        else:
            return False
    except Exception as e:
        return False


def _fd_server_check(ip_address):
    config = get_system_config()
    for item in config['fd_server']:
        if item['ip_address'] in ip_address:
            return True
    return False
