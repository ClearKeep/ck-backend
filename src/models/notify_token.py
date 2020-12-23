from src.models.base import db
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship, backref, load_only
from sqlalchemy import ForeignKey

class NotifyToken(db.Model):
    __tablename__ = 'notify_token'
    id = db.Column(db.String(36), primary_key=True)
    client_id = db.Column(db.String(36), ForeignKey('user.id'))
    device_id = db.Column(db.String(255), nullable=False)
    device_type = db.Column(db.String(16), nullable=False)
    push_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    user = relationship('User', back_populates='tokens')

    def add(self):
        client_device = self.get(self.client_id, self.device_id)
        if client_device is not None:
            self.id = client_device.id
            self.update()
        else:
            self.id = str(uuid.uuid4())
            db.session.add(self)
            db.session.commit()
        return self

    def get(self, client_id, device_id):
        client_device = self.query.filter_by(client_id=client_id, device_id=device_id).one_or_none()
        return client_device

    def update(self):
        db.session.merge(self)
        db.session.commit()