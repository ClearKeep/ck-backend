from src.models.note import Note
import uuid
from utils.logger import logger
from msg.message import Message
from datetime import datetime


class NoteService:

    """Docstring for NoteService. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__()

    def create_note(self, user_id, title, content, note_type):
        try:
            self.note = Note(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                content=content,
                note_type=note_type,
                created_by=user_id
            )
            self.note.add()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.CREATE_NOTE_FAILED)

    def edit_note(self, note_id, title, content, note_type, user_id):
        """TODO: Docstring for edit_note.

        :note_id: TODO
        :title: TODO
        :content: TODO
        :returns: TODO

        """
        try:
            self.note = Note().get(note_id)
            self.note.title = title
            self.note.content = content
            self.note.note_type = note_type
            self.note.updated_by = user_id
            self.note.updated_at = datetime.now()
            self.note.update()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.EDIT_NOTE_FAILED)

    def delete_note(self, note_id):
        """TODO: Docstring for delete_note.

        :note_id: TODO
        :returns: TODO

        """
        try:
            self.note = Note().get(note_id)
            self.note.delete()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.DELETE_NOTE_FAILED)
