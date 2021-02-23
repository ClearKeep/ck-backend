import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import Database


class NotifyToken(Database.get().Model):
    __tablename__ = 'notify_token'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    client_id = Database.get().Column(Database.get().String(36), ForeignKey('user.id'))
    device_id = Database.get().Column(Database.get().String(255), nullable=False)
    device_type = Database.get().Column(Database.get().String(16), nullable=False)
    push_token = Database.get().Column(Database.get().String(255), nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    user = relationship('User', back_populates='tokens')

    def add(self):
        client_device = self.get(self.client_id, self.device_id)
        if client_device is not None:
            self.id = client_device.id
            self.update()
        else:
            self.id = str(uuid.uuid4())
            try:
                Database.get().session.add(self)
                #Database.get().session.commit()
            except:
                Database.get().session.rollback()
                raise
        return self

    def get(self, client_id, device_id):
        client_device = self.query.filter_by(client_id=client_id, device_id=device_id).one_or_none()
        Database.get().session.commit()
        return client_device

    def get_client(self, client_id):
        client_tokens = self.query.filter_by(client_id=client_id).all()
        Database.get().session.commit()
        return client_tokens

    def get_clients(self, client_ids):
        client_tokens = self.query.filter(NotifyToken.client_id.in_(client_ids)).all()
        Database.get().session.commit()
        return client_tokens

    def update(self):
        try:
            Database.get().session.merge(self)
            #Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise

    def delete(self):
        try:
            Database.get().session.delete(self)
            #Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise