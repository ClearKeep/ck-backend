from firebase_admin import messaging
from src.models.notify_token import NotifyToken
from protos import notify_push_pb2
from middlewares.request_logged import *
from src.services.base import BaseService
from pushjack import APNSClient

class NotifyPushService(BaseService):
    def __init__(self):
        super().__init__(NotifyToken())
        self.client = APNSClient(certificate='configs/apns/certificate.pem>',
                            default_error_timeout=10,
                            default_expiration_offset=2592000,
                            default_batch_size=100,
                            default_retries=5)

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

    def ios_data_notification(self, registration_token, payload):
        alert = 'request_call'
        token = registration_token
        response = self.client.send(token,
              alert,
              badge='badge count',
              sound='sound to play',
              category='category',
              content_available=True,
              title='Title',
              title_loc_key='t_loc_key',
              title_loc_args='t_loc_args',
              action_loc_key='a_loc_key',
              loc_key='loc_key',
              extra={'custom': 'data'})
        self.client.close()
        print('{0} messages were sent successfully'.format(response.success_count))