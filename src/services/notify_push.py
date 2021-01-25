from firebase_admin import messaging
from kalyke.client import VoIPClient, APNsClient
from kalyke.payload import PayloadAlert, Payload

from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.config import get_system_config
from utils.logger import logger

class NotifyPushService(BaseService):
    def __init__(self):
        super().__init__(NotifyToken())
        self.client_ios_voip = VoIPClient(
            auth_key_filepath=get_system_config()["device_ios"].get('certificates_voip'),
            bundle_id= get_system_config()["device_ios"].get('bundle_id'),
            use_sandbox=get_system_config()["device_ios"].get('use_sandbox')
            )

        self.client_ios_chat = APNsClient(
            team_id= get_system_config()["device_ios"].get('team_id'),
            auth_key_id= get_system_config()["device_ios"].get('auth_key_id'),
            auth_key_filepath=get_system_config()["device_ios"].get('certificates_apns'),
            bundle_id= get_system_config()["device_ios"].get('bundle_id'),
            use_sandbox=get_system_config()["device_ios"].get('use_sandbox'),
            force_proto="h2",
            apns_push_type="alert"
            )
        if get_system_config()["device_ios"].get('use_sandbox'):
            logger.info("Device ios use sanbox for Development")
        else:
            logger.info("Device ios use sanbox for Production")
        logger.info(get_system_config()["device_ios"].get('certificates'))

    def register_token(self, client_id, device_id, device_type, push_token):
        self.model = NotifyToken(
            client_id=client_id,
            device_id=device_id,
            device_type=device_type,
            push_token=push_token,
        )
        return self.model.add()

    def android_text_notifications(self, registration_tokens, payload):
        message = messaging.MulticastMessage(
            tokens=registration_tokens,
            notification=payload
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


    def android_data_notification(self, registration_tokens, payload):
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

    def ios_data_notification(self, registration_tokens, payload):
        try:
            for token in registration_tokens:
                res = self.client_ios_voip.send_message(token, payload)
        except Exception as e:
            logger.info(e)

    def ios_text_notifications(self, registration_tokens, payload):
        alert = Payload(alert=payload, badge=1, sound="default")
        try:
            self.client_ios_chat.send_bulk_message(registration_tokens, alert)
        except Exception as e:
            logger.info(e)


