from functools import wraps
from utils.keycloak import KeyCloakUtils
import grpc
from utils.config import get_system_config
from msg.message import Message
import json
import logging
logger = logging.getLogger(__name__)


def auth_required(f):
    @wraps(f)
    async def wrap(*args, **kwargs):
        context = args[2]
        metadata = dict(context.invocation_metadata())
        # client request with access_token
        if 'access_token' in metadata:
            if _token_check(metadata['access_token']):
                return await f(*args, **kwargs)
            else:
                logger.error('Require authen inside metadata for : {}'.format(json.dumps(metadata)))
                errors = [Message.get_error_object(Message.INVALID_ACCESS_TOKEN)]
                context.set_details(json.dumps(errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.INTERNAL)
                return
        # server request with domain.
        logger.info('peer context: ' + json.dumps(context.peer()))
        if _fd_server_check(context.peer()):
            return await f(*args, **kwargs)
        return await f(*args, **kwargs)

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
        logger.error("Error in _token_check", exc_info=True)
        return False


def _fd_server_check(ip_address):
    config = get_system_config()
    for item in config['fd_server']:
        logger.info({"ip_address": item.get('ip_address', "Not found")})
        if item['ip_address'] in ip_address:
            return True
    return False
