from proto import signal_pb2
from src.controllers.base import *
from src.services.signal import SignalService, client_queue
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.message import MessageService


class SignalController(BaseController):
    def __init__(self, *kwargs):
        self.service = SignalService()

    @request_logged
    def PeerRegisterClientKey(self, request, context):
        try:
            self.service.peer_register_client_key(request)
            return signal_pb2.BaseResponse(success=True)
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

    @request_logged
    def GroupRegisterClientKey(self, request, context):
        print('***** CLIENT REGISTER KEY GROUP *****')
        print(request)
        try:
            self.service.group_register_client_key(request)
            return signal_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_GROUP_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
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

    @request_logged
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
            lst_client_key.append(client_key)

        response = signal_pb2.GroupGetAllClientKeyResponse(
            groupId=group_id,
            lstClientKey=lst_client_key
        )
        return response