from datetime import datetime
from src.models.base import Database
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.user import User


class MessageUserRead(Database.get().Model):
    __tablename__ = 'message_user_read'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    message_id = Database.get().Column(Database.get().String(36), ForeignKey('message.id'))
    client_id = Database.get().Column(Database.get().String(36), ForeignKey('user.id'))
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    user = relationship('User', back_populates='messages_read')
    message = relationship('Message', back_populates='users_read')


    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        return self


    def get_by_message_id(self, message_id):
        message_user_read = Database.get_session().query(MessageUserRead) \
            .filter(MessageUserRead.message_id == message_id) \
            .one_or_none()
        if message_user_read:
            message_user_read.get().session.remove()
        return message_user_read
