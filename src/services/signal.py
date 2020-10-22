from src.models.signal import SignalKey
from src.services.base import BaseService
from queue import Queue

client_store = {}
client_queue = {}

class SignalService(BaseService):
    def __init__(self):
        super().__init__(None)

    def register_bundle_key(self, request):
        client_combine_key = SignalKey(request.clientId, request.registrationId, request.deviceId,
                                       request.identityKeyPublic, request.preKeyId, request.preKey,
                                       request.signedPreKeyId, request.signedPreKey, request.signedPreKeySignature)
        client_store[client_combine_key.client_id] = client_combine_key

    def get_bundle_key_by_user_id(self, client_id):
        if client_id in client_store:
            return client_store[client_id]
        return None

    def subscribe(self, client_id):
        client_queue[client_id] = Queue()
