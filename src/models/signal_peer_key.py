from datetime import datetime

from sqlalchemy import ForeignKey

from src.models.base import Database


class PeerClientKey(Database.get().Model):
    __tablename__ = 'peer_client_key'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    device_id = Database.get().Column(Database.get().Integer, unique=False, nullable=False)
    registration_id = Database.get().Column(Database.get().Integer, unique=False, nullable=False)
    identity_key_public = Database.get().Column(Database.get().Binary)
    prekey_id = Database.get().Column(Database.get().Integer, unique=False, nullable=False)
    prekey = Database.get().Column(Database.get().Binary)
    signed_prekey_id = Database.get().Column(Database.get().Integer, unique=False, nullable=False)
    signed_prekey = Database.get().Column(Database.get().Binary)
    signed_prekey_signature = Database.get().Column(Database.get().Binary)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, client_id, registration_id, device_id, identity_key_public, prekey_id, prekey, signed_prekey_id,
                signed_prekey, signed_prekey_signature):
        self.client_id = client_id
        self.registration_id = registration_id
        self.device_id = device_id
        self.identity_key_public = identity_key_public
        self.prekey_id = prekey_id
        self.prekey = prekey
        self.signed_prekey_id = signed_prekey_id
        self.signed_prekey = signed_prekey
        self.signed_prekey_signature = signed_prekey_signature
        return self

    def add(self):
        client = self.get_by_client_id(client_id=self.client_id)
        if client is not None:
            self.id = client.id
            self.update()
        else:
            try:
                Database.get().session.add(self)
                #Database.get().session.commit()
            except:
                Database.get().session.rollback()
                raise

    def get_by_client_id(self, client_id):
        client = self.query.filter_by(client_id=client_id).one_or_none()
        Database.get().session.commit()
        return client

    def update(self):
        try:
            Database.get().session.merge(self)
            #Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise
