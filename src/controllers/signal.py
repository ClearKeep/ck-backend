from proto import signalc_pb2
from src.controllers.base import *
from src.services.signal import SignalService, client_queue
from middlewares.permission import *
from utils.logger import *


class SignalController(BaseController):
    def __init__(self, *kwargs):
        self.service = SignalService()

    def RegisterBundleKey(self, request, context):
        print('***** CLIENT REGISTER KEYS *****')
        print(request)
        try:
            self.service.register_bundle_key(request)
            return signalc_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            # return signalc_pb2.BaseResponse()

    def GetKeyBundleByUserId(self, request, context):
        client_id = request.clientId
        obj_resp = self.service.get_bundle_key_by_user_id(client_id)
        if obj_resp is not None:
            response = signalc_pb2.SignalKeysUserResponse(
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
        # return signalc_pb2.SignalKeysUserResponse()

    def Publish(self, request, context):
        try:
            # if request.receiveId in  client_queue
            client_queue[request.receiveId].put(request)
            return signalc_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            # return signalc_pb2.BaseResponse()

    def Listen(self, request, context):
        if request.clientId in client_queue:
            while True:
                publication = client_queue[request.clientId].get()  # blocking until the next .put for this queue
                publication_response = signalc_pb2.Publication(message=publication.message,
                                                               senderId=publication.senderId)
                yield publication_response

    def Subscribe(self, request, context):
        try:
            self.service.subscribe(request.clientId)
            return signalc_pb2.BaseResponse(message='success')
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
            # return signalc_pb2.BaseResponse()
