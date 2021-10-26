from datetime import datetime

from src.models.base import Database
from src.models.message_user_read import MessageUserRead
from sqlalchemy.orm import relationship, joinedload
from utils.logger import *


class Message(Database.get().Model):
    __tablename__ = 'message'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    group_id = Database.get().Column(Database.get().Integer, nullable=True)
    from_client_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    from_client_workspace_domain = Database.get().Column(Database.get().String(100), unique=False, nullable=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    client_workspace_domain = Database.get().Column(Database.get().String(100), unique=False, nullable=True)
    message = Database.get().Column(Database.get().Binary)
    sender_message = Database.get().Column(Database.get().Binary)
    message_type = Database.get().Column(
        Database.get().String(128),
        default='text',
        nullable=False
    )
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    deleted_at = Database.get().Column(Database.get().DateTime, nullable=True)
    users_read = relationship('MessageUserRead', back_populates='message')

    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        return self

    def get(self, message_id):
        message = Database.get_session().query(Message) \
            .filter(Message.id == message_id) \
            .one_or_none()
        Database.get().session.remove()
        return message

    def get_message_in_group(self, group_id, offset, from_time):
        message = Database.get_session().query(Message) \
            .options(joinedload(Message.users_read).joinedload(MessageUserRead.user)) \
            .filter(Message.group_id == group_id)

        if from_time != 0:
            dt = datetime.fromtimestamp(from_time / 1000)  # from time in milisecond => second
            message = message.filter(Message.created_at > dt)
        message = message.order_by(Message.created_at.desc())
        result = message.all()
        Database.get().session.remove()
        return result

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)
