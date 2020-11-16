from src.models.base import db
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_group_id = db.Column(db.String(36), unique=False, nullable=True)
    conversation_peer_id = db.Column(db.String(36), unique=False, nullable=True)
    from_client_id = db.Column(db.String(36), unique=False, nullable=True)
    message = db.Column(db.Binary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    # def get(self, group_id, client_id):
    #     client = self.query.filter_by(group_id=group_id, client_id=client_id).one_or_none()
    #     return client
    #
    # def get_all_in_group(self, group_id):
    #     client = self.query.filter_by(group_id=group_id).all()
    #     return client

    def update(self):
        db.session.merge(self)
        db.session.commit()
