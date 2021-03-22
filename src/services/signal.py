from src.models.signal_peer_key import PeerClientKey
from src.models.signal_group_key import GroupClientKey
from src.services.base import BaseService
from queue import Queue
from src.services.message import client_message_queue
from src.services.notify_inapp import NotifyInAppService

client_queue = {}


class SignalService(BaseService):
    def __init__(self):
        super().__init__(None)
        self.group_model = GroupClientKey()
        self.peer_model = PeerClientKey()

    def peer_register_client_key(self, request):
        client_peer_key = PeerClientKey().set_key(request.clientId, request.registrationId, request.deviceId,
                                                  request.identityKeyPublic, request.preKeyId, request.preKey,
                                                  request.signedPreKeyId, request.signedPreKey,
                                                  request.signedPreKeySignature)
        client_peer_key.add()
        # Check chatting available and push notify inapp for refreshing key
        self.client_update_key_notify(request.clientId)

    def peer_get_client_key(self, client_id):
        # if client_id in client_store:
        #     return client_store[client_id]
        return self.peer_model.get_by_client_id(client_id)

    def group_register_client_key(self, request):
        client_group_key = GroupClientKey().set_key(request.groupId, request.clientId, request.deviceId,
                                                    request.clientKeyDistribution)
        client_group_key.add()

    def group_get_client_key(self, group_id, client_id):
        client_key = self.group_model.get(group_id, client_id)
        if client_key and client_key.client_key:
            return client_key
        return None

    def group_get_all_client_key(self, group_id):
        return self.group_model.get_all_in_group(group_id)

    def client_update_key_notify(self, client_id):
        lst_group_peer = self.model.get_joined_group_type(client_id, "peer")
        notify_inapp_service = NotifyInAppService()
        for group_peer in lst_group_peer:
            if group_peer.group_clients:
                for client_peer_id in group_peer.group_clients:
                    if client_peer_id != client_id:
                        message_channel = "{}/message".format(client_peer_id)
                        if message_channel in client_message_queue:
                            notify_inapp_service.notify_client_update_peer_key(client_peer_id, client_id, group_peer.id)
