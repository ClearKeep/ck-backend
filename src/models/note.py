from datetime import datetime
from src.models.base import Database
from sqlalchemy.orm import relationship, joinedload

import logging
logger = logging.getLogger(__name__)
class Note(Database.get().Model):
    __tablename__ = 'note'
    id = Database.get().Column(
        Database.get().String(36), primary_key=True
    )
    user_id = Database.get().Column(
        Database.get().String(36), unique=False,
        nullable=True
    )
    title = Database.get().Column(
        Database.get().String(36), unique=False,
        nullable=True
    )
    content = Database.get().Column(Database.get().Binary)
    note_type = Database.get().Column(
        Database.get().String(128),
        default='text',
        nullable=False
    )
    created_by = Database.get().Column(
        Database.get().String(36), unique=False, nullable=True)
    created_at = Database.get().Column(
        Database.get().DateTime, default=datetime.now)
    updated_by = Database.get().Column(
        Database.get().String(36), unique=False, nullable=True)
    updated_at = Database.get().Column(
        Database.get().DateTime, onupdate=datetime.now, nullable=True)
    deleted_at = Database.get().Column(
        Database.get().DateTime, nullable=True)

    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        return self

    def get(self, note_id):
        note = Database.get_session().query(Note) \
            .filter(Note.id == note_id) \
            .one_or_none()
        Database.get().session.remove()
        return note

    def get_user_notes(self, user_id):
        user_notes = Database.get_session().query(Note) \
            .filter(Note.user_id == user_id) \
            .all()
        Database.get().session.remove()
        return user_notes

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

    def delete(self):
        try:
            Database.get_session().delete(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)
