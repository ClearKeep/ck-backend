from src.models.signal import SignalKey
from src.services.base import BaseService
from queue import Queue

#client_store = {}
client_queue = {}

class SignalService(BaseService):
    def __init__(self):
        super().__init__(SignalKey())

    def register_bundle_key(self, request):
        client_signal_key = SignalKey().set_keys(request.clientId, request.registrationId, request.deviceId,
                                       request.identityKeyPublic, request.preKeyId, request.preKey,
                                       request.signedPreKeyId, request.signedPreKey, request.signedPreKeySignature)
        #client_store[client_signal_key.client_id] = client_signal_key
        client_signal_key.add()


    def get_bundle_key_by_user_id(self, client_id):
        # if client_id in client_store:
        #     return client_store[client_id]
        return self.model.get_by_client_id(client_id)

    def subscribe(self, client_id):
        client_queue[client_id] = Queue()
