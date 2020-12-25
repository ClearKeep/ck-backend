from firebase_admin import messaging
from kalyke.client import VoIPClient

from src.models.notify_token import NotifyToken
from src.services.base import BaseService
from utils.config import get_system_config


class NotifyPushService(BaseService):
    def __init__(self):
        super().__init__(NotifyToken())
        self.client_ios = VoIPClient(
            auth_key_filepath=get_system_config()["device_ios"].get('certificates'),
            bundle_id= get_system_config()["device_ios"].get('bundle_id'),
            use_sandbox=True
            )
        print(get_system_config()["device_ios"].get('certificates'))

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
        print('{0} messages were sent successfully'.format(response.success_count))
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(registration_tokens[idx])
            print('List of tokens that caused failures: {0}'.format(failed_tokens))


    def android_data_notification(self, registration_tokens, payload):
        message = messaging.MulticastMessage(
            tokens=registration_tokens,
            data=payload,
            android=messaging.AndroidConfig(
                priority="high"
            )
        )
        response = messaging.send_multicast(message)
        print('{0} messages were sent successfully'.format(response.success_count))
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(registration_tokens)
            print('List of tokens that caused failures: {0}'.format(failed_tokens))

    def ios_data_notification(self, registration_tokens, payload):
        try:
            for token in registration_tokens:
                res = self.client_ios.send_message(token, payload)
        except Exception as e:
            print(e)
