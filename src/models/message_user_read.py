from datetime import datetime
from src.models.base import Database


class MessageUserRead(Database.get().Model):
    __tablename__ = 'message_user_read'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    message_id = Database.get().Column(Database.get().String(36), nullable=False)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)

    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        return self

    def add_all(self, lst_message):
        Database.get_session().add_all(lst_message)
