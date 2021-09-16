import protos.auth_pb2 as auth_messages
from src.controllers.base import BaseController
from src.services.auth import AuthService
from src.services.user import UserService
from src.services.message import MessageService
from src.services.signal import SignalService
from src.services.notify_inapp import NotifyInAppService
from utils.encrypt import EncryptUtils
from middlewares.permission import *
from middlewares.request_logged import *
from utils.config import *


class AuthController(BaseController):
    def __init__(self, *kwargs):
        self.service = AuthService()
        self.user_service = UserService()

    @request_logged
    async def login(self, request, context):
        try:
            token = self.service.token(request.email, request.hash_password)
            if token:
                introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
                user_id = introspect_token['sub']
                require_update_client_key, hash_password_salt = self.user_service.validate_hash_pass(user_id, request.hash_pass)
                require_actions = ['update_client_key'] if require_update_client_key else []
                mfa_state = self.user_service.get_mfa_state(user_id=user_id)
                hash_key = EncryptUtils.encoded_hash(
                    request.hash_password, user_id
                )
                if not mfa_state:
                    ### check if login require otp check
                    self.user_service.update_last_login(user_id=user_id)
                    client_key_obj = SignalService().peer_get_client_key(user_id)
                    client_key_peer = auth_messages.PeerGetClientKeyResponse(
                                            clientId=user_id,
                                            workspace_domain=get_owner_workspace_domain(),
                                            registrationId=client_key_obj.registration_id,
                                            deviceId=client_key_obj.device_id,
                                            identityKeyPublic=client_key_obj.identity_key_public,
                                            preKeyId=client_key_obj.prekey_id,
                                            preKey=client_key_obj.prekey,
                                            signedPreKeyId=client_key_obj.signed_prekey_id,
                                            signedPreKey=client_key_obj.signed_prekey,
                                            signedPreKeySignature=client_key_obj.signed_prekey_signature,
                                            identityKeyEncrypted=client_key_obj.identity_key_encrypted
                                        )
                    require_action_mess = ', '.join(require_actions)
                    auth_message = auth_messages.AuthRes(
                                        workspace_domain=get_owner_workspace_domain(),
                                        workspace_name=get_system_config()['server_name'],
                                        access_token=token['access_token'],
                                        expires_in=token['expires_in'],
                                        refresh_expires_in=token['refresh_expires_in'],
                                        refresh_token=token['refresh_token'],
                                        token_type=token['token_type'],
                                        session_state=token['session_state'],
                                        scope=token['scope'],
                                        hash_key=hash_key,
                                        require_action=require_action_mess,
                                        salt=hash_password_salt,
                                        client_key_peer = client_key_peer
                                    )
                else:
                    pre_access_token = self.service.create_otp_service(user_id)
                    require_actions += ["mfa_validate_otp"]
                    require_action_mess = ', '.join(require_actions)
                    auth_message = auth_messages.AuthRes(
                                        salt=hash_password_salt,
                                        workspace_domain=get_owner_workspace_domain(),
                                        workspace_name=get_system_config()['server_name'],
                                        hash_key=hash_key,
                                        sub=user_id,
                                        pre_access_token=pre_access_token,
                                        require_action=require_action_mess
                                    )
                return auth_message
            else:
                raise Exception(Message.AUTH_USER_NOT_FOUND)

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def login_google(self, request, context):
        try:
            token, is_new_user = self.service.google_login(request.id_token)
            if not token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            user_id = introspect_token['sub']
            hash_key = EncryptUtils.encoded_hash(introspect_token['sub'], introspect_token['sub'])
            require_action_mess = "verify_pincode" if not is_new_user else "register_pincode"
            pre_access_token = self.service.hash_pre_access_token(user_id, require_action_mess)
            auth_response = auth_messages.AuthRes(
                                salt=hash_password_salt,
                                workspace_domain=get_owner_workspace_domain(),
                                workspace_name=get_system_config()['server_name'],
                                hash_key=hash_key,
                                sub=user_id,
                                pre_access_token=pre_access_token,
                                require_action=require_action_mess
                            )
            return auth_response
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def login_office(self, request, context):
        try:
            token, is_new_user = self.service.office_login(request.access_token)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if not token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            user_id = introspect_token['sub']
            hash_key = EncryptUtils.encoded_hash(introspect_token['sub'], introspect_token['sub'])
            require_action_mess = "verify_pincode" if not is_new_user else "register_pincode"
            pre_access_token = self.service.hash_pre_access_token(user_id, require_action_mess)
            auth_response = auth_messages.AuthRes(
                                salt=hash_password_salt,
                                workspace_domain=get_owner_workspace_domain(),
                                workspace_name=get_system_config()['server_name'],
                                hash_key=hash_key,
                                sub=user_id,
                                pre_access_token=pre_access_token,
                                require_action=require_action_mess
                            )
            return auth_response
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def login_facebook(self, request, context):
        try:
            token, is_new_user = self.service.facebook_login(request.access_token)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            if not token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
            user_id = introspect_token['sub']
            hash_key = EncryptUtils.encoded_hash(introspect_token['sub'], introspect_token['sub'])
            require_action_mess = "verify_pincode" if not is_new_user else "register_pincode"
            pre_access_token = self.service.hash_pre_access_token(user_id, require_action_mess)
            auth_response = auth_messages.AuthRes(
                                salt=hash_password_salt,
                                workspace_domain=get_owner_workspace_domain(),
                                workspace_name=get_system_config()['server_name'],
                                hash_key=hash_key,
                                sub=user_id,
                                pre_access_token=pre_access_token,
                                require_action=require_action_mess
                            )
            return auth_response
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def register(self, request, context):
        # check exist user
        try:
            exists_user = self.service.get_user_by_email(request.email)
            if exists_user:
                raise Exception(Message.REGISTER_USER_ALREADY_EXISTS)

            # register new user on keycloak
            new_user_id = self.service.register_user(request.email, request.hash_password, request.display_name)

            if not new_user_id:
                # self.service.delete_user(new_user_id)
                raise Exception(Message.REGISTER_USER_FAILED)

            # create new user in database
            new_user = UserService().create_new_user(new_user_id, request.email, request.display_name, request.hash_password, request.salt,  'account')
            if new_user is None:
                self.service.delete_user(new_user_id)
                raise Exception(Message.REGISTER_USER_FAILED)
            try:
                SignalService().peer_register_client_key(new_user_id, request.client_key_peer)
            except Exception:
                self.service.delete_user(new_user_id)
                UserService().delete_user(new_user_id)
                raise Exception(Message.REGISTER_USER_FAILED)

            return auth_messages.RegisterRes()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.REGISTER_USER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def fogot_password(self, request, context):
        try:
            self.service.send_forgot_password(request.email)
            return auth_messages.BaseResponse()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    @request_logged
    async def logout(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']
            device_id = request.device_id
            refresh_token = request.refresh_token
            self.service.remove_token(client_id=user_id, device_id=device_id)
            MessageService().un_subscribe(user_id)
            NotifyInAppService().un_subscribe(user_id)
            self.service.logout(refresh_token)
            # KeyCloakUtils.remove_session(
            #     session_id=introspect_token['session_state']
            # )

            return auth_messages.BaseResponse()

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def validate_otp(self, request, context):
        try:
            success_status, token = self.service.verify_otp(request.user_id, request.otp_hash, request.otp_code)
            if not success_status:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            introspect_token = KeyCloakUtils.introspect_token(token["access_token"])
            require_action = ""
            client_key_obj = SignalService().peer_get_client_key(user_id)
            client_key_peer = auth_messages.PeerGetClientKeyResponse(
                                    clientId=user_id,
                                    workspace_domain=get_owner_workspace_domain(),
                                    registrationId=client_key_obj.registration_id,
                                    deviceId=client_key_obj.device_id,
                                    identityKeyPublic=client_key_obj.identity_key_public,
                                    preKeyId=client_key_obj.prekey_id,
                                    preKey=client_key_obj.prekey,
                                    signedPreKeyId=client_key_obj.signed_prekey_id,
                                    signedPreKey=client_key_obj.signed_prekey,
                                    signedPreKeySignature=client_key_obj.signed_prekey_signature,
                                    identityKeyEncrypted=client_key_obj.identity_key_encrypted
                                )
            return auth_messages.AuthRes(
                workspace_domain=get_owner_workspace_domain(),
                workspace_name=get_system_config()['server_name'],
                access_token=token["access_token"],
                expires_in=token['expires_in'],
                refresh_expires_in=token['refresh_expires_in'],
                refresh_token=token['refresh_token'],
                token_type=token['token_type'],
                session_state=token['session_state'],
                scope=token['scope'],
                require_action = require_action,
                client_key_peer=client_key_peer
            )

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def resend_otp(self, request, context):
        try:
            otp_hash = self.service.resend_otp(request.user_id, request.otp_hash)
            return auth_messages.MfaResendOtpRes(
                                success=True,
                                otp_hash=otp_hash
                            )

        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                # basic exception dont have any args / exception raised by some library may contains some args, but will not in listed message
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def register_pincode(self, request, context):
        try:
            success_status, token = self.service.verify_hash_pre_access_token(request.user_id, request.pre_access_token, "register_pincode")
            # get temp request
            old_client_key_obj = SignalService().peer_get_client_key(request.user_id)
            require_action_mess = "verify_pincode"
            pre_access_token = self.service.hash_pre_access_token(request.user_id, require_action_mess)
            SignalService().peer_register_client_key(request.user_id, request.client_key_peer)
            try:
                UserService().update_hash_pin(request.user_id, request.hash_pincode, request.salt)
            except Exception as e:
                logger.error(e)
                old_client_key_peer = auth_messages.PeerGetClientKeyResponse(
                                                    clientId=request.user_id,
                                                    workspace_domain=get_owner_workspace_domain(),
                                                    registrationId=old_client_key_obj.registration_id,
                                                    deviceId=old_client_key_obj.device_id,
                                                    identityKeyPublic=old_client_key_obj.identity_key_public,
                                                    preKeyId=old_client_key_obj.prekey_id,
                                                    preKey=old_client_key_obj.prekey,
                                                    signedPreKeyId=old_client_key_obj.signed_prekey_id,
                                                    signedPreKey=old_client_key_obj.signed_prekey,
                                                    signedPreKeySignature=old_client_key_obj.signed_prekey_signature,
                                                    identityKeyEncrypted=old_client_key_obj.identity_key_encrypted
                                                )
                SignalService().peer_register_client_key(user_id, old_client_key_peer)
                raise Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)

            return auth_messages.RegisterPincodeRes(
                        user_id = request.user_id,
                        pre_access_token = pre_access_token,
                        require_action = require_action_mess
                    )
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def verify_pincode(self, request, context):
        try:
            success_status, token = self.service.verify_hash_pre_access_token(request.user_id, request.pre_access_token, "verify_pincode")
            if not success_status:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            success_status, hash_pincode_salt = self.user_service.validate_hash_pass(request.user_id, request.hash_pincode)
            if not success_status:
                # should change message here
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            introspect_token = KeyCloakUtils.introspect_token(token["access_token"])
            require_action = ""
            client_key_obj = SignalService().peer_get_client_key(user_id)
            client_key_peer = auth_messages.PeerGetClientKeyResponse(
                                    clientId=user_id,
                                    workspace_domain=get_owner_workspace_domain(),
                                    registrationId=client_key_obj.registration_id,
                                    deviceId=client_key_obj.device_id,
                                    identityKeyPublic=client_key_obj.identity_key_public,
                                    preKeyId=client_key_obj.prekey_id,
                                    preKey=client_key_obj.prekey,
                                    signedPreKeyId=client_key_obj.signed_prekey_id,
                                    signedPreKey=client_key_obj.signed_prekey,
                                    signedPreKeySignature=client_key_obj.signed_prekey_signature,
                                    identityKeyEncrypted=client_key_obj.identity_key_encrypted
                                )
            return auth_messages.AuthRes(
                workspace_domain=get_owner_workspace_domain(),
                workspace_name=get_system_config()['server_name'],
                access_token=token["access_token"],
                expires_in=token['expires_in'],
                refresh_expires_in=token['refresh_expires_in'],
                refresh_token=token['refresh_token'],
                token_type=token['token_type'],
                session_state=token['session_state'],
                scope=token['scope'],
                salt=hash_pincode_salt,
                client_key_peer = client_key_peer
            )
            # get temp request
            old_client_key_obj = SignalService().peer_get_client_key(user_id)
            try:
                UserService().update_hash_pin(user_id, request.hash_pincode, request.salt)
            except Exception as e:
                logger.error(e)
                raise Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)
            client_key_obj = SignalService().peer_get_client_key(user_id)
            client_key_peer = auth_messages.PeerGetClientKeyResponse(
                          clientId=user_id,
                          workspace_domain=get_owner_workspace_domain(),
                          registrationId=client_key_obj.registration_id,
                          deviceId=client_key_obj.device_id,
                          identityKeyPublic=client_key_obj.identity_key_public,
                          preKeyId=client_key_obj.prekey_id,
                          preKey=client_key_obj.prekey,
                          signedPreKeyId=client_key_obj.signed_prekey_id,
                          signedPreKey=client_key_obj.signed_prekey,
                          signedPreKeySignature=client_key_obj.signed_prekey_signature,
                          identityKeyEncrypted=client_key_obj.identity_key_encrypted
                      )
        except Exception as e:
            logger.error(e)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
