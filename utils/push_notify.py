from kalyke.client import VoIPClient, APNsClient
from utils.config import get_system_config
import firebase_admin
from firebase_admin import credentials, messaging
from utils.logger import logger
from kalyke.payload import PayloadAlert, Payload
import time

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
        logger.error(e)
        raise Exception(e)


async def ios_text_notifications(registration_token, payload):
    alert = Payload(alert=payload, badge=1, sound="default")
    try:
        expiration = int(time.time()) + 10
        res = await client_ios_text._send_message(registration_token, alert, expiration=expiration)
        logger.info("Push iOS text notify success with token: {}".format(registration_token))
        logger.info(res)
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
        raise Exception(e)

# async def ios_data_multi_notification(registration_tokens, payload):
#     for token in registration_tokens:
#         try:
#             expiration = int(time.time()) + 10
#             res = await client_ios_voip._send_message(token, payload, expiration=expiration)
#             logger.info("Push iOS data notify success with token: {}".format(token))
#         except Exception as e:
#             logger.error(e)


# def android_text_notifications(registration_tokens, payload):
#     message = messaging.MulticastMessage(
#         tokens=registration_tokens,
#         notification=payload,
#         android=messaging.AndroidConfig(
#             priority="normal",
#             ttl=10
#         )
#     )
#     response = messaging.send_multicast(message)
#     logger.info('{0} messages were sent successfully'.format(response.success_count))
#     if response.failure_count > 0:
#         responses = response.responses
#         failed_tokens = []
#         for idx, resp in enumerate(responses):
#             if not resp.success:
#                 # The order of responses corresponds to the order of the registration tokens.
#                 failed_tokens.append(registration_tokens[idx])
#         logger.info('List of tokens that caused failures: {0}'.format(failed_tokens))


# def android_data_multi_notification(registration_tokens, payload):
#     message = messaging.MulticastMessage(
#         tokens=registration_tokens,
#         data=payload,
#         android=messaging.AndroidConfig(
#             priority="high",
#             ttl=10
#         )
#     )
#     response = messaging.send_multicast(message)
#     logger.info('{0} messages were sent successfully'.format(response.success_count))
#     if response.failure_count > 0:
#         responses = response.responses
#         failed_tokens = []
#         for idx, resp in enumerate(responses):
#             if not resp.success:
#                 # The order of responses corresponds to the order of the registration tokens.
#                 failed_tokens.append(registration_tokens)
#         logger.info('List of tokens that caused failures: {0}'.format(failed_tokens))
