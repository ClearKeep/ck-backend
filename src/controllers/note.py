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
            self.service.create_note(
                user_id,
                request.title,
                request.content,
                request.note_type
            )
            return note_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            return note_pb2.BaseResponse(
                    success=False,
                    errors=note_pb2.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
                )

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
            return note_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            return note_pb2.BaseResponse(
                    success=False,
                    errors=note_pb2.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
                )

    async def delete_note(self, request, context):
        """docstring for create_note"""
        try:
            self.service.delete_note(
                request.note_id
            )
            return note_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(e.args[0])]
            return note_pb2.BaseResponse(
                    success=False,
                    errors=note_pb2.ErrorRes(
                        code=errors[0].code,
                        message=errors[0].message
                    )
                )
