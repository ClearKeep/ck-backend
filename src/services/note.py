from src.models.note import Note
import uuid
from utils.logger import logger
from msg.message import Message
from datetime import datetime

class NoteService:

    """NoteService for creating/editing/getting/deleting note. """

    def __init__(self):
        super().__init__()

    def create_note(self, user_id, title, content, note_type):
        # creating note for user_id, with informations: title, content and note_type
        try:
            self.note = Note(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                content=content,
                note_type=note_type,
                created_by=user_id
            )
            return self.note.add()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.CREATE_NOTE_FAILED)

    def edit_note(self, note_id, title, content, note_type, user_id):
        # editing note with changing informations: title, content, note_type, user_id
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
        # delete note
        try:
            self.note = Note().get(note_id)
            self.note.delete()
        except Exception as e:
            logger.error(e)
            raise Exception(Message.DELETE_NOTE_FAILED)

    def get_user_notes(self, user_id):
        # get all note of user
        try:
            user_notes = Note().get_user_notes(user_id)
            return user_notes
        except Exception as e:
            logger.error(e)
            raise Exception(Message.GET_USER_NOTES_FAILED)
