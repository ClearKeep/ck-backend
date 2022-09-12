from utils.config import get_system_config
import firebase_admin
from firebase_admin import credentials, messaging
from apns2.client import APNsClient
from apns2.payload import Payload
from utils.const import DeviceType
import time
import asyncio
from functools import wraps
import logging
logger = logging.getLogger(__name__)

push_clients = {
    "android": {},
    "ios": {}
}


def _ios_retry(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        retry = 0
        while retry <= 1:
            try:
                await func(*args, **kwargs)
            except Exception as e:
                logger.debug("retry push ios")
                logger.debug(e, exc_info=True)
                push_clients[DeviceType.ios] = {}
                retry += 1
            else:
                break

    return wrapper


@_ios_retry
async def ios_data_notification(registration_token, data, end_user_env):
    loop = asyncio.get_running_loop()
    def _run_in_executor():
        topic = _get_topic(end_user_env) + '.voip'
        expiration = int(time.time()) + 10
        apns_client = _get_push_client("ios", end_user_env)["voip"]
        payload = Payload(custom={'publication': data})
        apns_client.send_notification(registration_token, payload, topic, expiration=expiration)

    await loop.run_in_executor(None, _run_in_executor)
    logger.info("Push iOS data notify success with token: {}".format(registration_token))


@_ios_retry
async def ios_text_notifications(registration_token, alert, data, end_user_env):
    loop = asyncio.get_running_loop()
    def _run_in_executor():
        payload = Payload(
            alert=alert,
            badge=1,
            sound="default",
            mutable_content=1,
            custom={'publication': data}
        )
        topic = _get_topic(end_user_env)
        expiration = int(time.time()) + 10
        apns_client = _get_push_client(DeviceType.ios, end_user_env)["alert"]
        apns_client.send_notification(registration_token, payload, topic, expiration=expiration)

    await loop.run_in_executor(None, _run_in_executor)
    logger.info("Push iOS text notify success with token: {}".format(registration_token))


async def android_data_notification(registration_token, payload, end_user_env):
    loop = asyncio.get_running_loop()
    app = _get_push_client(DeviceType.android, end_user_env)
    message = messaging.Message(
        token=registration_token,
        data=payload,
        android=messaging.AndroidConfig(
            priority="high",
            ttl=10
        )
    )
    try:
        response = await loop.run_in_executor(None, lambda: messaging.send(message, app=app))
        logger.info('Android data notification')
        logger.info(response)
    except Exception as e:
        logger.debug(e, exc_info=True)


def _get_topic(end_user_env):
    config = get_system_config()["notification"]
    if not end_user_env or end_user_env not in config[DeviceType.ios]:
        if end_user_env:
            logger.debug('end_user_env not set')
        end_user_env = 'default'
    return config[DeviceType.ios][end_user_env]["bundle_id"]


def _get_push_client(device_type, end_user_env):
    config = get_system_config()["notification"]
    if not end_user_env or end_user_env not in config[DeviceType.ios]:
        if end_user_env:
            logger.debug('end_user_env not set')
        end_user_env = 'default'

    if end_user_env not in push_clients[device_type]:
        if device_type == DeviceType.android:
            cred = credentials.Certificate(config[DeviceType.android][end_user_env]['fire_base_config'])
            push_clients[device_type][end_user_env] = firebase_admin.initialize_app(cred, name=end_user_env)
        elif device_type == DeviceType.ios:
            ios_config = config[DeviceType.ios][end_user_env]
            push_clients[device_type][end_user_env] = {
                "alert": APNsClient(
                    ios_config["certificates_apns"], 
                    use_sandbox=ios_config["use_sandbox"],
                    use_alternative_port=False
                ),
                "voip": APNsClient(
                    ios_config["certificates_voip"], 
                    use_sandbox=ios_config["use_sandbox"],
                    use_alternative_port=False
                ),
            }
    return push_clients[device_type][end_user_env]