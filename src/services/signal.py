from src.models.signal_peer_key import PeerClientKey
from src.models.signal_group_key import GroupClientKey
from src.services.base import BaseService
from src.services.message import client_message_queue
from src.services.notify_inapp import NotifyInAppService
from src.models.group import GroupChat
import ast
from msg.message import Message

client_queue = {}


class SignalService(BaseService):
    def __init__(self):
        super().__init__(None)
        self.group_client_key_model = GroupClientKey()
        self.peer_model = PeerClientKey()
        self.group_chat_model = GroupChat()

    def peer_register_client_key(self, request):
        client_peer_key = PeerClientKey().set_key(request.clientId, request.registrationId, request.deviceId,
                                                  request.identityKeyPublic, request.preKeyId, request.preKey,
                                                  request.signedPreKeyId, request.signedPreKey,
                                                  request.signedPreKeySignature)
        client_peer_key.add()
        # Check chatting available and push notify inapp for refreshing key
        self.client_update_key_notify(request.clientId)

    def peer_get_client_key(self, client_id):
        return self.peer_model.get_by_client_id(client_id)

    def group_register_client_key(self, client_id, request):
        client_group_key = GroupClientKey().set_key(request.groupId, client_id, None, None, request.deviceId,
                                                    request.clientKeyDistribution, request.identityKeyEncrypted)
        new_group_key = client_group_key.add()
        if new_group_key is None:
            raise Exception(Message.REGISTER_CLIENT_GROUP_FAILED_AVAILABLE)

    def group_bulk_update_client_key(self, client_id, list_group_client_key):
        is_updated = GroupClientKey().update_bulk_client_key(client_id, list_group_client_key)
        if not is_updated:
            raise Exception(Message.UPDATE_CLIENT_KEY_GROUPS_FAILED)

    def group_get_client_key(self, group_id, client_id):
        client_key = self.group_client_key_model.get(group_id, client_id)
        if client_key:
            return client_key
        return None

    def group_by_owner_get_client_key(self, group_id, client_id):
        client_key = self.group_chat_model.get_client_key_by_owner_group(group_id, client_id)
        if client_key:
            return client_key
        return None

    def group_get_all_client_key(self, group_id):
        return self.group_client_key_model.get_all_in_group(group_id)

    def client_update_key_notify(self, client_id):
        lst_group_peer = self.group_chat_model.get_joined_group_type(client_id, "peer")
        notify_inapp_service = NotifyInAppService()
        for group_peer in lst_group_peer:
            if group_peer.group_clients:
                lst_client_id = ast.literal_eval(group_peer.group_clients)
                for client_peer_id in lst_client_id:
                    if client_peer_id != client_id:
                        message_channel = "{}/message".format(client_peer_id)
                        if message_channel in client_message_queue:
                            notify_inapp_service.notify_client_update_peer_key(client_peer_id, client_id, group_peer.id)
