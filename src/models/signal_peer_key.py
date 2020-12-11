from src.models.base import db
from datetime import datetime


class PeerClientKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), unique=False, nullable=False)
    device_id = db.Column(db.Integer, unique=False, nullable=False)
    registration_id = db.Column(db.Integer, unique=False, nullable=False)
    identity_key_public = db.Column(db.Binary)
    prekey_id = db.Column(db.Integer, unique=False, nullable=False)
    prekey = db.Column(db.Binary)
    signed_prekey_id = db.Column(db.Integer, unique=False, nullable=False)
    signed_prekey = db.Column(db.Binary)
    signed_prekey_signature = db.Column(db.Binary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, client_id, registration_id, device_id, identity_key_public, prekey_id, prekey, signed_prekey_id, signed_prekey, signed_prekey_signature):
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
            db.session.add(self)
            db.session.commit()

    def get_by_client_id(self, client_id):
        client = self.query.filter_by(client_id=client_id).one_or_none()
        return client

    def update(self):
        db.session.merge(self)
        db.session.commit()
