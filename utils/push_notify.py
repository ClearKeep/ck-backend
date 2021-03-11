from kalyke.client import VoIPClient, APNsClient
from utils.config import get_system_config
import firebase_admin
from firebase_admin import credentials, messaging
from utils.logger import logger
from kalyke.payload import PayloadAlert, Payload


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


async def ios_data_notification(registration_tokens, payload):
    for token in registration_tokens:
        try:
            res = await client_ios_voip._send_message(token, payload)
            logger.info("Push iOS data notify success with token: {}".format(token))
        except Exception as e:
            logger.error(e)


async def ios_text_notifications(registration_tokens, payload, data=None):
    alert = Payload(alert=payload, badge=1, sound="default", custom=data)
    for token in registration_tokens:
        try:
            #res = client_ios_text.send_message(token, alert)
            res = await client_ios_text._send_message(token, alert)
            logger.info("Push iOS text notify success with token: {}".format(token))
        except Exception as e:
            logger.error(e)


# init push service for Android
cred = credentials.Certificate(get_system_config()["device_android"].get("fire_base_config"))
default_app = firebase_admin.initialize_app(cred)


def android_text_notifications(registration_tokens, payload, data=None):
    message = messaging.MulticastMessage(
        tokens=registration_tokens,
        notification=payload,
        data=data

    )
    response = messaging.send_multicast(message)
    logger.info('{0} messages were sent successfully'.format(response.success_count))
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens[idx])
        logger.info('List of tokens that caused failures: {0}'.format(failed_tokens))


def android_data_notification(registration_tokens, payload):
    message = messaging.MulticastMessage(
        tokens=registration_tokens,
        data=payload,
        android=messaging.AndroidConfig(
            priority="high"
        )
    )
    response = messaging.send_multicast(message)
    logger.info('{0} messages were sent successfully'.format(response.success_count))
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens)
        logger.info('List of tokens that caused failures: {0}'.format(failed_tokens))
