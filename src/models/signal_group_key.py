from src.models.base import db
from datetime import datetime


class GroupClientKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(36), unique=False, nullable=False)
    client_id = db.Column(db.String(36), unique=False, nullable=False)
    device_id = db.Column(db.Integer, unique=False, nullable=False)
    client_key = db.Column(db.Binary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, group_id, client_id, device_id, client_key):
        self.group_id = group_id
        self.client_id = client_id
        self.device_id = device_id
        self.client_key = client_key
        return self

    def add(self):
        client = self.get(self.group_id, self.client_id)
        if client is not None:
            self.id = client.id
            self.update()
        else:
            db.session.add(self)
            db.session.commit()

    def get(self, group_id, client_id):
        client = self.query.filter_by(group_id=group_id, client_id=client_id).one_or_none()
        return client

    def get_all_in_group(self, group_id):
        client = self.query.filter_by(group_id=group_id).all()
        return client

    def update(self):
        db.session.merge(self)
        db.session.commit()
