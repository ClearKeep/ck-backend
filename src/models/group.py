from datetime import datetime
import secrets
from src.models.base import Database
from src.models.message import Message
from src.models.signal_group_key import GroupClientKey


class GroupChat(Database.get().Model):
    __tablename__ = 'group_chat'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    group_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    group_avatar = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    group_type = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    group_clients = Database.get().Column(Database.get().Text, unique=False, nullable=True)
    group_rtc_token = Database.get().Column(Database.get().Text, unique=False, nullable=True)
    created_by = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_by = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now, nullable=True)
    last_message_at = Database.get().Column(Database.get().DateTime, nullable=True)
    last_message_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    deleted_at = Database.get().Column(Database.get().DateTime, nullable=True)

    def add(self):
        try:
            Database.get().session.add(self)
            #Database.get().session.commit()
            return self
        except:
            Database.get().session.rollback()
            raise

    def get(self, group_id):
        group = Database.get().session.query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.id == group_id) \
            .one_or_none()
        return group

    def search(self, keyword):
        search = "%{}%".format(keyword)
        group = Database.get().session.query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.group_name.like(search)).all()
        return group

    def get_joined(self, client_id):
        result = Database.get().session.query(GroupChat, Message) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupClientKey.client_id == client_id) \
            .all()
        return result

    def get_joined_group_type(self, client_id, group_type):
        result = Database.get().session.query(GroupChat, GroupClientKey.id, GroupChat.group_clients) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .filter(GroupClientKey.client_id == client_id) \
            .filter(GroupChat.group_type == group_type) \
            .all()
        return result

    def update(self):
        try:
            Database.get().session.merge(self)
            #Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise

    def get_group_rtc_token(self, group_id):
        result = Database.get().session.query(GroupChat.group_rtc_token) \
            .filter(GroupChat.id == group_id) \
            .first()
        # result = self.query.filter_by(id=group_id).first()
        return result

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
