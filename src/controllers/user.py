import protos.user_pb2 as user_messages
from src.controllers.base import *
from src.services.auth import AuthService
from src.services.user import UserService
from src.services.signal import SignalService
from src.services.group import GroupService
from middlewares.permission import *
from middlewares.request_logged import *
from utils.logger import *
from utils.config import *
from client.client_user import *
import srp


class UserController(BaseController, user_pb2_grpc.UserServicer):
    def __init__(self, *kwargs):
        self.service = UserService()

    @auth_required
    async def request_change_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_name = introspect_token['preferred_username']
            user_info = self.service.get_user_by_auth_source(user_name, "account")
            if not user_info:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            password_verifier = bytes.fromhex(user_info.password_verifier)
            salt = bytes.fromhex(user_info.salt)
            client_public = bytes.fromhex(request.client_public)

            srv = srp.Verifier(user_name, salt, password_verifier, client_public)
            s, B = srv.get_challenge()
            # need store private b of server

            server_private = srv.get_ephemeral_secret().hex()
            user_info.srp_server_private = server_private
            user_info.update()

            public_challenge_b = B.hex()
            auth_challenge_res = user_messages.RequestChangePasswordRes(
                salt=user_info.salt,
                public_challenge_b=public_challenge_b
            )
            return auth_challenge_res

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def change_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_name = introspect_token['preferred_username']
            client_session_key_proof = request.client_session_key_proof
            user_info = self.service.get_user_by_auth_source(user_name, "account")

            if not user_info:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            password_verifier = bytes.fromhex(user_info.password_verifier)
            salt = bytes.fromhex(user_info.salt)
            client_session_key_proof_bytes = bytes.fromhex(client_session_key_proof)

            srv = srp.Verifier(username=user_name, bytes_s=salt, bytes_v=password_verifier, bytes_A=bytes.fromhex(request.client_public), bytes_b=bytes.fromhex(user_info.srp_server_private))
            srv.verify_session(client_session_key_proof_bytes)
            authenticated = srv.authenticated()
            if not authenticated:
                raise Exception(Message.AUTHENTICATION_FAILED)

            self.service.change_password(request, user_info.password_verifier, request.hash_password, introspect_token['sub']) # update for keycloak

            try:
                old_identity_key_encrypted = SignalService().client_update_identity_key(introspect_token["sub"], request.identity_key_encrypted)
            except Exception as e:
                logger.error(e, exc_info=True)
                self.service.change_password(request, request.hash_password, user_info.password_verifier, introspect_token['sub'])
                raise Exception(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)
            try:
                salt, iv_parameter = self.service.update_hash_pass(introspect_token["sub"], request.hash_password, request.salt, request.iv_parameter)
            except Exception as e:
                logger.error(e, exc_info=True)
                self.service.change_password(request, request.hash_password, request.password_verifier, introspect_token['sub'])
                SignalService().client_update_identity_key(introspect_token["sub"], old_identity_key_encrypted)
                raise Exception(Message.REGISTER_CLIENT_SIGNAL_KEY_FAILED)
            user_sessions = KeyCloakUtils.get_sessions(user_id=introspect_token["sub"])
            for user_session in user_sessions:
                if user_session['id'] != introspect_token['session_state']:
                    KeyCloakUtils.remove_session(session_id=user_session['id'])
            return user_messages.BaseResponse()

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CHANGE_PASSWORD_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def get_mfa_state(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            mfa_enable = self.service.get_mfa_state(client_id)
            return  user_messages.MfaStateResponse(mfa_enable=mfa_enable,)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def disable_mfa(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            if not introspect_token or 'sub' not in introspect_token:
                raise Exception(Message.AUTH_USER_NOT_FOUND)
            client_id = introspect_token['sub']
            success, next_step = self.service.init_mfa_state_disabling(client_id)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def enable_mfa(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            user_info = self.service.get_user_by_id(client_id)

            if user_info.phone_number is None:
                success = False
                next_step = 'mfa_update_phone_number'
            else:
                success, next_step = self.service.init_mfa_state_enabling(client_id)
            return user_messages.MfaBaseResponse(success=success,next_step=next_step)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def mfa_auth_challenge(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            email = introspect_token['preferred_username']

            self.service.mfa_validate_password_flow(client_id)
            user_info = self.service.get_user_by_id(client_id)
            password_verifier = bytes.fromhex(user_info.password_verifier)
            salt = bytes.fromhex(user_info.salt)
            client_public = bytes.fromhex(request.client_public)

            srv = srp.Verifier(email, salt, password_verifier, client_public)
            s, B = srv.get_challenge()

            server_private = srv.get_ephemeral_secret().hex()
            user_info.srp_server_private = server_private
            user_info.update()

            public_challenge_b = B.hex()

            auth_challenge_res = user_messages.MfaAuthChallengeResponse(
                salt=user_info.salt,
                public_challenge_b=public_challenge_b
            )
            return auth_challenge_res
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def mfa_validate_password(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            user_info = self.service.get_user_by_id(client_id)

            client_session_key_proof = request.client_session_key_proof
            user_name = introspect_token['preferred_username']
            phone_number = user_info.phone_number
            password_verifier = bytes.fromhex(user_info.password_verifier)
            salt = bytes.fromhex(user_info.salt)
            client_session_key_proof_bytes = bytes.fromhex(client_session_key_proof)

            srv = srp.Verifier(username=user_name, bytes_s=salt, bytes_v=password_verifier, bytes_A=bytes.fromhex(request.client_public), bytes_b=bytes.fromhex(user_info.srp_server_private))
            srv.verify_session(client_session_key_proof_bytes)
            authenticated = srv.authenticated()

            if not authenticated:
                raise Exception(Message.AUTHENTICATION_FAILED)
            success, next_step = self.service.mfa_request_otp(client_id, phone_number)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.OTP_SERVER_NOT_RESPONDING)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def mfa_validate_otp(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            success, next_step = self.service.validate_otp(client_id, request.otp)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MFA_STATE_FALED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def mfa_resend_otp(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            success, next_step = self.service.re_init_otp(client_id)
            return user_messages.MfaBaseResponse(success=success, next_step=next_step)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.OTP_SERVER_NOT_RESPONDING)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def get_profile(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            user_info = self.service.get_profile(client_id)
            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_PROFILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @auth_required
    async def update_profile(self, request, context):
        logger.info("user update_profile api")
        try:
            display_name = request.display_name
            avatar = request.avatar
            phone_number = request.phone_number
            clear_phone_number = request.clear_phone_number

            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            await self.service.update_profile(client_id, display_name, phone_number, avatar, clear_phone_number)
            return user_messages.BaseResponse()

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPDATE_PROFILE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @auth_required
    # @request_logged
    async def get_user_info(self, request, context):
        try:
            client_id = request.client_id
            client_workspace_domain = request.workspace_domain
            owner_workspace_domain = get_owner_workspace_domain()

            if client_workspace_domain == owner_workspace_domain:
                user_info = self.service.get_user_info(client_id, owner_workspace_domain)
            else:
                client = ClientUser(client_workspace_domain)
                user_info = await client.get_user_info(client_id=client_id, workspace_domain=client_workspace_domain)

            if user_info is not None:
                return user_info
            else:
                errors = [Message.get_error_object(Message.USER_NOT_FOUND)]
                context.set_details(json.dumps(
                    errors, default=lambda x: x.__dict__))
                context.set_code(grpc.StatusCode.NOT_FOUND)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_USER_INFO_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def search_user(self, request, context):
        logger.info("user search_user api")
        try:
            keyword = request.keyword
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            obj_res = self.service.search_user(keyword, client_id)
            return obj_res

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def get_users(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            owner_workspace_domain = get_owner_workspace_domain()
            obj_res = self.service.get_users(client_id, owner_workspace_domain)
            return obj_res

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def find_user_by_email(self, request, context):
        try:
            return await self.service.find_user_by_email(request.email)
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.FIND_USER_BY_EMAIL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def find_user_detail_info_from_email_hash(self, request, context):
        try:
            logger.debug(f'find_user_detail_info_from_email_hash, {request=}, {context=}')
            obj_res = self.service.find_user_detail_info_from_email_hash(request.email_hash)
            return obj_res
        except Exception as e:
            logger.error("find_user_detail_info_from_email_hash", exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.FIND_USER_BY_EMAIL_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def get_user_domain(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            domain = "server.domain2"
            obj_res = self.service.get_users_domain(domain=domain)
            return obj_res

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.SEARCH_USER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # update status for user ("Active, Busy, Away, Do not disturb")
    @request_logged
    @auth_required
    async def update_status(self, request, context):
        logger.info("user update_status api")
        try:
            status = request.status
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            self.service.set_user_status(client_id, status)
            return user_messages.BaseResponse()

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.UPDATE_USER_STATUS_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def ping_request(self, request, context):
        logger.info("ping_request api")
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            self.service.update_client_record(client_id)
            return user_messages.BaseResponse()

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.PING_PONG_SERVER_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def get_clients_status(self, request, context):
        logger.info("get_client_status api")
        try:
            list_clients = request.lst_client
            should_get_profile = request.should_get_profile
            return await self.service.get_list_clients_status(list_clients,should_get_profile)

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_USER_STATUS_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def upload_avatar(self, request, context):
        logger.info("upload_avatar api")
        try:
            file_name = request.file_name
            file_content = request.file_data
            file_content_type = request.file_content_type
            file_hash = request.file_hash
            # client_id from headers
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            obj_res = self.service.upload_avatar(client_id, file_name, file_content, file_content_type, file_hash)
            return obj_res

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_USER_STATUS_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def delete_account(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            user_info = self.service.get_user_by_id(client_id)
            await GroupService().forgot_peer_groups_for_client(user_info)
            await GroupService().member_forgot_password_in_group(user_info)
            SignalService().delete_client_peer_key(client_id)
            AuthService().delete_user(client_id)
            UserService().delete_user(client_id)
            return user_messages.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.DELETE_ACCOUNT_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_update_display_name(self, request, context):
        try:
            await self.service.workspace_update_display_name(
                user_id=request.user_id,
                display_name=request.display_name
            )
            return user_messages.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_find_user_by_email(self, request, context):
        try:
            return self.service.find_user_by_email_here(email=request.email)
        except Exception as e:
            logger.error(e, exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
