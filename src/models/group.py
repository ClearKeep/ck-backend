from src.models.base import db
from datetime import datetime
from src.models.signal_group_key import GroupClientKey
import uuid

class GroupChat(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    group_name = db.Column(db.String(255), unique=False, nullable=True)
    group_avatar = db.Column(db.String(255), unique=False, nullable=True)
    created_by = db.Column(db.String(36), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_by = db.Column(db.String(36), unique=False, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        self.id = str(uuid.uuid4())
        db.session.add(self)
        db.session.commit()
        return self

    def get(self, group_id):
        group = self.query.filter_by(id=group_id).one_or_none()
        return group

    def search(self, keyword):
        search = "%{}%".format(keyword)
        group = self.query.filter(GroupChat.group_name.like(search)).all()
        return group

    def get_joined(self, client_id):
        result = self.query \
             .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
             .add_columns(GroupChat.id, GroupChat.group_name, GroupChat.group_avatar, GroupChat.created_by, GroupChat.created_at, GroupChat.updated_by, GroupChat.updated_at) \
             .filter(GroupClientKey.client_id == client_id) \
             .all()
        return result
        #     .filter(friendships.user_id == userID) \
        #     .paginate(page, 1, False)

    def update(self):
        db.session.merge(self)
        db.session.commit()

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
