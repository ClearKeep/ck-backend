from src.models.base import db
from datetime import datetime
from src.models.signal_group_key import GroupClientKey
from src.models.message import Message
import uuid


class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=False, nullable=True)
    group_avatar = db.Column(db.String(255), unique=False, nullable=True)
    group_type = db.Column(db.String(36), unique=False, nullable=True)
    group_clients = db.Column(db.Text, unique=False, nullable=True)
    created_by = db.Column(db.String(36), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_by = db.Column(db.String(36), unique=False, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=True)
    last_message_at = db.Column(db.DateTime, nullable=True)
    last_message_id = db.Column(db.String(36), unique=False, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        self.id = str(uuid.uuid4())
        db.session.add(self)
        db.session.commit()
        return self

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


    def update(self):
        db.session.merge(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
