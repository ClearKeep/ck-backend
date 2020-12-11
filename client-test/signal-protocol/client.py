from __future__ import print_function
import grpc
import threading
from proto import signal_pb2
from proto import signal_pb2_grpc
from libsignal.util.keyhelper import KeyHelper
from .store.mystore import MyStore
from libsignal.sessionbuilder import SessionBuilder
from libsignal.sessioncipher import SessionCipher
from libsignal.state.prekeybundle import PreKeyBundle
from libsignal.identitykeypair import IdentityKeyPair
from libsignal.identitykey import IdentityKey
from libsignal.ecc.djbec import DjbECPublicKey, DjbECPrivateKey
from libsignal.state.prekeyrecord import PreKeyRecord
from libsignal.state.signedprekeyrecord import SignedPreKeyRecord
from libsignal.protocol.prekeywhispermessage import PreKeyWhisperMessage


class ClientTest:
    def __init__(self, client_id, device_id, host, port):
        self.client_id = client_id
        self.device_id = device_id
        self.stub = self.grpc_stub(host, port)
        self.my_store = MyStore()


    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return signal_pb2_grpc.SignalKeyDistributionStub(channel)

    def register_keys(self, device_id, signed_prekey_id):
        # generate client pre key and store it
        client_prekeys_pair = KeyHelper.generatePreKeys(1, 2)
        client_prekey_pair = client_prekeys_pair[0]
        self.my_store.storePreKey(client_prekey_pair.getId(), client_prekey_pair)

        # generate client signed pre key and store it
        client_signed_prekey_pair = KeyHelper.generateSignedPreKey(self.my_store.getIdentityKeyPair(), signed_prekey_id)
        client_signed_prekey_signature = client_signed_prekey_pair.getSignature()
        self.my_store.storeSignedPreKey(signed_prekey_id, client_signed_prekey_pair)

        response = self.stub.PeerRegisterClientKey(signal_pb2.PeerRegisterClientKeyRequest(
            clientId=self.client_id,
            registrationId=self.my_store.getLocalRegistrationId(),
            deviceId=device_id,
            identityKeyPublic=self.my_store.getIdentityKeyPair().getPublicKey().serialize(),
            preKeyId=client_prekey_pair.getId(),
            preKey=client_prekey_pair.serialize(),
            signedPreKeyId=signed_prekey_id,
            signedPreKey=client_signed_prekey_pair.serialize(),
            signedPreKeySignature=client_signed_prekey_signature
        ))

        print("Client RegisterBundleKey received: " + response.message)

    def listen(self):
        threading.Thread(target=self.heard, daemon=True).start()

    def heard(self):
        request = signal_pb2.SubscribeAndListenRequest(clientId=self.client_id)
        for publication in self.stub.Listen(request):  # this line will wait for new messages from the server
            message_plain_text = self.decrypt_message(publication.message, publication.fromClientId)
            print("From {}: {}".format(publication.fromClientId, message_plain_text))

    def subscribe(self):
        request = signal_pb2.SubscribeAndListenRequest(clientId=self.client_id)
        response = self.stub.Subscribe(request)
        self.listen()

    def publish(self, message, receiver_id):
        # encrypt message first
        out_goging_message = self.encrypt_message(message, receiver_id)

        # send message
        request = signal_pb2.PublishRequest(clientId=receiver_id, message=out_goging_message, fromClientId=self.client_id)
        response = self.stub.Publish(request)

    def encrypt_message(self, message, receiver_id):
        # get sender client key first (need to store in second time)
        request_receiver_key = signal_pb2.PeerGetClientKeyRequest(clientId=receiver_id)
        response_receiver_key = self.stub.PeerGetClientKey(request_receiver_key)
        print("Encrypt Message - get receiver key from server =", response_receiver_key)

        # build session
        my_session_builder = SessionBuilder(self.my_store, self.my_store, self.my_store, self.my_store, receiver_id, 1)

        # combine key for receiver
        # identity public key
        receiver_identity_key_public = IdentityKey(DjbECPublicKey(response_receiver_key.identityKeyPublic[1:]))

        # pre key
        receiver_prekey = PreKeyRecord(serialized=response_receiver_key.preKey)

        # signed prekey
        receiver_signed_prekey_pair = SignedPreKeyRecord(serialized=response_receiver_key.signedPreKey)

        # combine prekey bundle
        receiver_prekey_bundle = PreKeyBundle(response_receiver_key.registrationId,
                                              response_receiver_key.deviceId,
                                              response_receiver_key.preKeyId,
                                              receiver_prekey.getKeyPair().getPublicKey(),
                                              response_receiver_key.signedPreKeyId,
                                              receiver_signed_prekey_pair.getKeyPair().getPublicKey(),
                                              response_receiver_key.signedPreKeySignature,
                                              receiver_identity_key_public)


        # process session and create session cipher
        my_session_builder.processPreKeyBundle(receiver_prekey_bundle)
        my_session_cipher = SessionCipher(self.my_store, self.my_store, self.my_store, self.my_store, receiver_id, 1)

        # encrypt message
        outgoing_message = my_session_cipher.encrypt(message)
        outgoging_message_serialize = outgoing_message.serialize()
        print("Encrypt Message - Out Going Message =", outgoging_message_serialize)
        # return encrypt message
        return outgoging_message_serialize

    def decrypt_message(self, message, sender_id):
        print("Decrypt Message - In Coming Message Encrypted=", message)
        incoming_message = PreKeyWhisperMessage(serialized=message)
        # init session to decrypt
        my_session_cipher = SessionCipher(self.my_store, self.my_store, self.my_store, self.my_store, sender_id, 1)
        message_plain_text = my_session_cipher.decryptPkmsg(incoming_message)
        # print("Decrypt Message - Plain Text Message =", message_plain_text)
        # return encrypt message
        return message_plain_text