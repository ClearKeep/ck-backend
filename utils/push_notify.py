from utils.config import get_system_config
import firebase_admin
from firebase_admin import credentials, messaging
from apns2.client import APNsClient
from apns2.payload import Payload
import time
import asyncio
import logging
logger = logging.getLogger(__name__)
# init push service for iOS
apns_voip_client = APNsClient(
    get_system_config()["device_ios"].get('certificates_voip'), 
    use_sandbox=get_system_config()["device_ios"].get('use_sandbox'),
    use_alternative_port=False
)

apns_client = APNsClient(
    get_system_config()["device_ios"].get('certificates_apns'),
    use_sandbox=get_system_config()["device_ios"].get('use_sandbox'),
    use_alternative_port=False
)

# init push service for Android
cred = credentials.Certificate(get_system_config()["device_android"].get("fire_base_config"))
default_app = firebase_admin.initialize_app(cred)


async def ios_data_notification(registration_token, payload):
    loop = asyncio.get_running_loop()
    topic = get_system_config()["device_ios"].get('bundle_id') + '.voip'
    try:
        expiration = int(time.time()) + 10
        await loop.run_in_executor(None, lambda: apns_voip_client.send_notification(registration_token, payload, topic, expiration=expiration))
        logger.info("Push iOS data notify success with token: {}".format(registration_token))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception(e)


async def ios_text_notifications(registration_token, alert, data):
    loop = asyncio.get_running_loop()
    payload = Payload(
        alert=alert,
        badge=1,
        sound="default",
        mutable_content=1,
        custom={'publication': data}
    )
    topic = get_system_config()["device_ios"].get('bundle_id')
    try:
        expiration = int(time.time()) + 10
        await loop.run_in_executor(None, lambda: apns_client.send_notification(registration_token, payload, topic, expiration=expiration))
        logger.info("Push iOS text notify success with token: {}".format(registration_token))
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception(e)


def android_data_notification(registration_token, payload):
    try:
        message = messaging.Message(
            token=registration_token,
            data=payload,
            android=messaging.AndroidConfig(
                priority="high",
                ttl=10
            )
        )
        response = messaging.send(message)
        logger.info('Android data notification')
        logger.info(response)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception(e)
