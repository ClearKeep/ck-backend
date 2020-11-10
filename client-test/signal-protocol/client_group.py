from __future__ import print_function
import grpc
import threading
from proto import signal_pb2, signal_pb2_grpc
from libsignal.axolotladdress import AxolotlAddress
from libsignal.groups.senderkeyname import SenderKeyName
from .store.mysenderkeystore import MySenderKeyStore
from libsignal.groups.groupsessionbuilder import GroupSessionBuilder
from libsignal.groups.groupcipher import GroupCipher
from libsignal.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage


class ClientGroupTest:
    def __init__(self, client_id, device_id, host, port):
        self.client_id = client_id
        self.device_id = device_id
        self.stub = self.grpc_stub(host, port)
        self.my_sender_store = MySenderKeyStore()
        self.my_sender_address = AxolotlAddress(client_id, device_id)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return signal_pb2_grpc.SignalKeyDistributionStub(channel)

    def register_group_keys(self, group_id):
        group_sender = SenderKeyName(group_id, self.my_sender_address);
        self.my_session_builder = GroupSessionBuilder(self.my_sender_store)
        my_sender_distribution_message = self.my_session_builder.create(group_sender)

        response = self.stub.GroupRegisterClientKey(signal_pb2.GroupRegisterClientKeyRequest(
            groupId=group_sender.groupId,
            clientId=self.client_id,
            deviceId=self.device_id,
            clientKeyDistribution=my_sender_distribution_message.serialize()
        ))
        print("REGISTER SENDER KEY GROUP RESPONSE: " + response.message)

    def listen(self):
        threading.Thread(target=self.heard, daemon=True).start()

    def heard(self):

        request = signal_pb2.SubscribeAndListenRequest(clientId=self.client_id)
        for publication in self.stub.Listen(request):  # this line will wait for new messages from the server
            print("publication=", publication)
            message_plain_text = self.decrypt_message(publication.message, publication.fromClientId, publication.groupId)
            print("From {}: {}".format(publication.fromClientId, message_plain_text))

    def subscribe(self):
        request = signal_pb2.SubscribeAndListenRequest(clientId=self.client_id)
        response = self.stub.Subscribe(request)
        self.listen()

    def publish(self, message, group_id):
        # encrypt message first
        out_goging_message = self.encrypt_message(message, group_id)
        # send message
        request = signal_pb2.PublishRequest(fromClientId=self.client_id, groupId=group_id, message=out_goging_message)
        response = self.stub.Publish(request)

    def encrypt_message(self, message, group_id):
        group_sender = SenderKeyName(group_id, self.my_sender_address)
        my_group_cipher = GroupCipher(self.my_sender_store, group_sender)
        out_going_message = my_group_cipher.encrypt(message)
        #out_goging_message_serialize = out_going_message.serialize()
        print("Encrypt Message - Out Going Message =", out_going_message)
        # return encrypt message
        return out_going_message

    def decrypt_message(self, message, from_client_id, group_id):
        print("Decrypt Message - In Coming Message Encrypted=", message)
        # get sender key first

        request = signal_pb2.GroupGetClientKeyRequest(groupId=group_id, clientId=from_client_id)
        response = self.stub.GroupGetClientKey(request)
        received_sender_distribution_message = SenderKeyDistributionMessage(serialized=response.clientKey.clientKeyDistribution);

        sender_address = AxolotlAddress(response.clientKey.clientId, response.clientKey.deviceId)
        group_sender = SenderKeyName(group_id, sender_address)
        sender_key_record = self.my_sender_store.loadSenderKey(group_sender)
        if sender_key_record.isEmpty():
            print("Decrypt Message - call process", message)
            self.my_session_builder.process(group_sender, received_sender_distribution_message)

        my_group_cipher = GroupCipher(self.my_sender_store, group_sender)
        message_plain_text = my_group_cipher.decrypt(message)
        # return encrypt message
        return message_plain_text
