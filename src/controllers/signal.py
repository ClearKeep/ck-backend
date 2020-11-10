from proto import signal_pb2
from src.controllers.base import *
from src.services.signal import SignalService, client_queue
from middlewares.permission import *
from utils.logger import *


class SignalController(BaseController):
    def __init__(self, *kwargs):
        self.service = SignalService()

    def PeerRegisterClientKey(self, request, context):
        print('***** CLIENT REGISTER KEYS *****')
        print(request)
        try:
            self.service.peer_register_client_key(request)
            return signal_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)


    def PeerGetClientKey(self, request, context):
        client_id = request.clientId
        obj_resp = self.service.peer_get_client_key(client_id)
        if obj_resp is not None:
            response = signal_pb2.PeerGetClientKeyResponse(
                clientId=client_id,
                registrationId=obj_resp.registration_id,
                deviceId=obj_resp.device_id,
                identityKeyPublic=obj_resp.identity_key_public,
                preKeyId=obj_resp.prekey_id,
                preKey=obj_resp.prekey,
                signedPreKeyId=obj_resp.signed_prekey_id,
                signedPreKey=obj_resp.signed_prekey,
                signedPreKeySignature=obj_resp.signed_prekey_signature
            )
            return response

        errors = [Message.get_error_object(Message.CLIENT_SIGNAL_KEY_NOT_FOUND)]
        context.set_details(json.dumps(
            errors, default=lambda x: x.__dict__))
        context.set_code(grpc.StatusCode.NOT_FOUND)


    def GroupRegisterClientKey(self, request, context):
        print('***** CLIENT REGISTER KEY GROUP *****')
        print(request)
        try:
            self.service.group_register_client_key(request)
            return signal_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_GROUP_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    def GroupGetClientKey(self, request, context):
        group_id = request.groupId
        client_id = request.clientId
        obj_resp = self.service.group_get_client_key(group_id, client_id)
        if obj_resp is not None:
            response = signal_pb2.GroupGetClientKeyResponse(
                groupId=obj_resp.group_id,
                clientKey=signal_pb2.GroupClientKeyObject(
                    clientId=obj_resp.client_id,
                    deviceId=obj_resp.device_id,
                    clientKeyDistribution=obj_resp.client_key
                )
            )
            return response

        errors = [Message.get_error_object(Message.CLIENT_SIGNAL_KEY_NOT_FOUND)]
        context.set_details(json.dumps(
            errors, default=lambda x: x.__dict__))
        context.set_code(grpc.StatusCode.NOT_FOUND)

    def GroupGetAllClientKey(self, request, context):
        group_id = request.groupId
        lst_client = self.service.group_get_all_client_key(group_id)
        lst_client_key = []
        for client in lst_client:
            client_key = signal_pb2.GroupClientKeyObject(
                clientId=client.client_id,
                deviceId=client.device_id,
                clientKeyDistribution=client.client_key
            )
            lst_client.append(client_key)

        response = signal_pb2.GroupGetAllClientKeyResponse(
            groupId=group_id,
            lstClientKey=lst_client_key
        )
        return response


    def Publish(self, request, context):
        try:
            group_id = request.groupId
            if group_id:
                lst_client = self.service.group_get_all_client_key(group_id)
                for client in lst_client:
                    if client.client_id != request.fromClientId:
                        client_queue[client.client_id].put(request)
            else:
                client_queue[request.clientId].put(request)
            return signal_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)


    def Listen(self, request, context):
        if request.clientId in client_queue:
            while True:
                publication = client_queue[request.clientId].get()  # blocking until the next .put for this queue
                publication_response = signal_pb2.Publication(fromClientId=publication.fromClientId, groupId=publication.groupId,
                                                               message=publication.message)
                yield publication_response


    def Subscribe(self, request, context):
        try:
            self.service.subscribe(request.clientId)
            return signal_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
