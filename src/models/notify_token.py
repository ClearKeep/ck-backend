import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import db


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
            try:
                db.session.add(self)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
        return self

    def get(self, client_id, device_id):
        client_device = self.query.filter_by(client_id=client_id, device_id=device_id).one_or_none()
        return client_device

    def get_client(self, client_id):
        client_tokens = self.query.filter_by(client_id=client_id).all()
        return client_tokens

    def get_clients(self, client_ids):
        client_tokens = self.query.filter(NotifyToken.client_id.in_(client_ids)).all()
        return client_tokens

    def update(self):
        try:
            db.session.merge(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()