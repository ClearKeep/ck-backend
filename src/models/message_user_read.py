from datetime import datetime
from src.models.base import Database
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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

    # def add_all(self, lst_message):
    #     Database.get_session().add_all(lst_message)
