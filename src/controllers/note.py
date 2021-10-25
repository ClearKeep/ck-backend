from src.controllers.base import BaseController
from src.services.note import NoteService
from utils.keycloak import KeyCloakUtils
import protos.note_pb2 as note_pb2
from utils.logger import logger
from msg.message import Message


class NoteController(BaseController):

    """Docstring for NoteController. """

    def __init__(self, *args):
        """TODO: to be defined.

        :*args: TODO

        """
        BaseController.__init__(self, NoteService())

    async def create_note(self, request, context):
        """docstring for create_note"""
        try:
            metadata = dict(context.invocation_metadata())
            access_token_information = KeyCloakUtils.introspect_token(
                metadata['access_token']
            )
            user_id = access_token_information['sub']
            # user_id = '081f2345-bcc8-4447-9da8-3b1e04ad6c51'
            note = self.service.create_note(
                user_id,
                request.title,
                request.content,
                request.note_type
            )
            return note_pb2.UserNoteResponse(
                id=note.id,
                title=note.title,
                content=note.content,
                note_type=note.note_type,
                created_at=int(note.created_at.timestamp() * 1000)
            )

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

    async def edit_note(self, request, context):
        """docstring for create_note"""
        try:
            metadata = dict(context.invocation_metadata())
            access_token_information = KeyCloakUtils.introspect_token(
                metadata['access_token']
            )
            user_id = access_token_information['sub']
            # user_id = '081f2345-bcc8-4447-9da8-3b1e04ad6c51'
            self.service.edit_note(
                request.note_id,
                request.title,
                request.content,
                request.note_type,
                user_id
            )
            return note_pb2.BaseResponse()

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

    async def delete_note(self, request, context):
        """docstring for create_note"""
        try:
            self.service.delete_note(
                request.note_id
            )
            return note_pb2.BaseResponse()

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

    async def get_user_notes(self, request, context):
        """docstring for create_note"""
        try:
            metadata = dict(context.invocation_metadata())
            access_token_information = KeyCloakUtils.introspect_token(
                metadata['access_token']
            )
            user_id = access_token_information['sub']
            # user_id = '081f2345-bcc8-4447-9da8-3b1e04ad6c51'
            user_notes = self.service.get_user_notes(
                user_id
            )
            return note_pb2.GetUserNotesResponse(
                user_notes=[note_pb2.UserNoteResponse(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    note_type=note.note_type,
                    created_at=int(note.created_at.timestamp() * 1000)
                ) for note in user_notes],
                base_response=note_pb2.BaseResponse()
            )

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
