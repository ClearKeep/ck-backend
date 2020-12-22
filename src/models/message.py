from src.models.base import db
from datetime import datetime
from utils.config import get_system_config


class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    group_id = db.Column(db.Integer, unique=False, nullable=True)
    from_client_id = db.Column(db.String(36), unique=False, nullable=True)
    client_id = db.Column(db.String(36), unique=False, nullable=True)
    message = db.Column(db.Binary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_message_in_group(self, group_id, offset, from_time):
        client = self.query.filter_by(group_id=group_id)
        if from_time != 0:
            dt = datetime.fromtimestamp(from_time/1000) #from time in milisecond => second
            client = client.filter(Message.created_at > dt)

        client = client.order_by(Message.created_at.desc())

        if offset != 0:
            limit = get_system_config()['page_limit']
            client = client.offset(offset).limit(limit)

        result = client.all()
        return result

    def update(self):
        db.session.merge(self)
        db.session.commit()
