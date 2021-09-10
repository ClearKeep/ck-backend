from protos import signal_pb2
from src.controllers.base import *
from src.services.signal import SignalService
from src.services.group import GroupService
from middlewares.permission import *
from middlewares.request_logged import *
from client.client_signal import *
from utils.config import get_owner_workspace_domain


class SignalController(BaseController):
    def __init__(self, *kwargs):
        self.service = SignalService()

    @request_logged
    async def PeerRegisterClientKey(self, request, context):
        try:
            self.service.peer_register_client_key(request)
            return signal_pb2.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def ClientUpdatePeerKey(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']
            if user_id == request.client_id:
                self.service.client_update_peer_key(request)
            return signal_pb2.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def PeerGetClientKey(self, request, context):
        header_data = dict(context.invocation_metadata())
        introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
        user_id = introspect_token['sub']

        client_id = request.clientId
        client_workspace_domain = request.workspace_domain
        owner_workspace_domain = get_owner_workspace_domain()
        if client_workspace_domain and client_workspace_domain != owner_workspace_domain:
            # get key from other server
            obj_resp = ClientSignal(client_workspace_domain).get_user_signal_key(client_id, client_workspace_domain)
            return obj_resp
        else:
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
                if user_id == client_id:
                    response.identityKeyEncrypted = obj_resp.identity_key_encrypted
                return response

            errors = [Message.get_error_object(Message.CLIENT_SIGNAL_KEY_NOT_FOUND)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.NOT_FOUND)

    @request_logged
    async def GroupRegisterClientKey(self, request, context):
        try:
            self.service.group_register_client_key(request)
            return signal_pb2.BaseResponse()
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_GROUP_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def GroupGetClientKey(self, request, context):
        group_id = request.groupId
        client_id = request.clientId
        # get group first
        group = GroupService().get_group_obj(group_id)
        owner_workspace_domain = get_owner_workspace_domain()
        if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
            owner_workspace_group_id = group.owner_group_id
            obj_resp = self.service.group_by_owner_get_client_key(owner_workspace_group_id, client_id)
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
            else:
                obj_resp = ClientSignal(group.owner_workspace_domain).group_get_client_key(group.owner_group_id, client_id)
                return obj_resp
        else:
            obj_resp = self.service.group_get_client_key(group_id, client_id)
            if obj_resp is not None:
                if obj_resp.client_workspace_domain and obj_resp.client_workspace_domain != owner_workspace_domain:
                    obj_resp = ClientSignal(obj_resp.client_workspace_domain).workspace_group_get_client_key(obj_resp.client_workspace_group_id, obj_resp.client_id)
                    return obj_resp
                else:
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
    async def WorkspaceGroupGetClientKey(self, request, context):
        print("WorkspaceGroupGetClientKey")
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
    #not use for now
    async def GroupGetAllClientKey(self, request, context):
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
