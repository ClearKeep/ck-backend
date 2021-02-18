from datetime import datetime
import secrets
from src.models.base import db
from src.models.message import Message
from src.models.signal_group_key import GroupClientKey


class GroupChat(db.Model):
    __tablename__ = 'group_chat'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=False, nullable=True)
    group_avatar = db.Column(db.String(255), unique=False, nullable=True)
    group_type = db.Column(db.String(36), unique=False, nullable=True)
    group_clients = db.Column(db.Text, unique=False, nullable=True)
    group_rtc_token = db.Column(db.Text, unique=False, nullable=True)
    created_by = db.Column(db.String(36), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_by = db.Column(db.String(36), unique=False, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=True)
    last_message_at = db.Column(db.DateTime, nullable=True)
    last_message_id = db.Column(db.String(36), unique=False, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            raise

    def get(self, group_id):
        group = db.session.query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.id == group_id) \
            .one_or_none()
        return group

    def search(self, keyword):
        search = "%{}%".format(keyword)
        group = db.session.query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.group_name.like(search)).all()
        return group

    def get_joined(self, client_id):
        result = db.session.query(GroupChat, Message) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupClientKey.client_id == client_id) \
            .all()
        return result

    def get_joined_group_type(self, client_id, group_type):
        result = db.session.query(GroupChat, GroupClientKey.id, GroupChat.group_clients) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .filter(GroupClientKey.client_id == client_id) \
            .filter(GroupChat.group_type == group_type) \
            .all()
        return result

    def update(self):
        try:
            db.session.merge(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def get_group_rtc_token(self, group_id):
        result = db.session.query(GroupChat.group_rtc_token) \
            .filter(GroupChat.id == group_id) \
            .first()
        # result = self.query.filter_by(id=group_id).first()
        return result

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
