from kalyke.client import VoIPClient, APNsClient
from utils.config import get_system_config
import firebase_admin
from firebase_admin import credentials, messaging
from kalyke.payload import PayloadAlert, Payload
import time
import logging
logger = logging.getLogger(__name__)
# init push service for iOS
client_ios_voip = VoIPClient(
    auth_key_filepath=get_system_config()["device_ios"].get('certificates_voip'),
    bundle_id=get_system_config()["device_ios"].get('bundle_id'),
    use_sandbox=get_system_config()["device_ios"].get('use_sandbox')
)

client_ios_text = APNsClient(
    team_id=get_system_config()["device_ios"].get('team_id'),
    auth_key_id=get_system_config()["device_ios"].get('auth_key_id'),
    auth_key_filepath=get_system_config()["device_ios"].get('certificates_apns'),
    bundle_id=get_system_config()["device_ios"].get('bundle_id'),
    use_sandbox=get_system_config()["device_ios"].get('use_sandbox'),
    force_proto="h2",
    apns_push_type="alert"
)

# init push service for Android
cred = credentials.Certificate(get_system_config()["device_android"].get("fire_base_config"))
default_app = firebase_admin.initialize_app(cred)


async def ios_data_notification(registration_token, payload):
    try:
        expiration = int(time.time()) + 10
        res_obj = await client_ios_voip._send_message(registration_token, payload, expiration=expiration)
        logger.info("Push iOS data notify success with token: {}".format(registration_token))
        logger.info(res_obj)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception(e)


async def ios_text_notifications(registration_token, alert, data):
    payload = Payload(
        alert=alert,
        badge=1,
        sound="default",
        mutable_content=1,
        custom={'publication': data}
    )
    try:
        expiration = int(time.time()) + 10
        res = await client_ios_text._send_message(registration_token, payload, expiration=expiration)
        logger.info("Push iOS text notify success with token: {}".format(registration_token))
        logger.info(res)
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
