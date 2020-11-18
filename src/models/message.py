from src.models.base import db
from datetime import datetime
from utils.config import get_system_config


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(36), unique=False, nullable=True)
    from_client_id = db.Column(db.String(36), unique=False, nullable=True)
    client_id = db.Column(db.String(36), unique=False, nullable=True)
    message = db.Column(db.Binary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    # def get_message_in_group(self, group_id):
    #     client = self.query.filter_by(group_id=group_id).all()
    #     return client

    def get_message_in_group(self, group_id, offset=0, from_time=None):
        client = self.query.filter_by(group_id=group_id)
        if from_time is not None:
            dt = datetime.fromtimestamp(from_time)
            client.filter(Message.created_at > dt)
        if offset != 0:
            client.offset(offset)
            client.limit(get_system_config["page_limit"])

        client.order_by(Message.created_at.desc())
        result = client.all()
        return result

    def update(self):
        db.session.merge(self)
        db.session.commit()
