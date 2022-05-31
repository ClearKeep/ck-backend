from datetime import datetime
from sqlalchemy import ForeignKey
from src.models.base import Database
import logging
logger = logging.getLogger(__name__)
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
    identity_key_encrypted = Database.get().Column(Database.get().String(255), unique=False)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, client_id, registration_id, device_id, identity_key_public, prekey_id, prekey, signed_prekey_id,
                signed_prekey, signed_prekey_signature, identity_key_encrypted):
        self.client_id = client_id
        self.registration_id = registration_id
        self.device_id = device_id
        self.identity_key_public = identity_key_public
        self.prekey_id = prekey_id
        self.prekey = prekey
        self.signed_prekey_id = signed_prekey_id
        self.signed_prekey = signed_prekey
        self.signed_prekey_signature = signed_prekey_signature
        self.identity_key_encrypted = identity_key_encrypted
        return self

    def get(self, id):
        client = Database.get_session().query(PeerClientKey) \
            .filter(PeerClientKey.id == id) \
            .one_or_none()
        Database.get().session.remove()
        return client

    def add(self):
        client = self.get_by_client_id(client_id=self.client_id)
        if client is not None:
            return False
        else:
            try:
                Database.get_session().add(self)
                Database.get_session().commit()
                return True
            except Exception as e:
                Database.get_session().rollback()
                logger.error(e)

    def get_by_client_id(self, client_id):
        client = Database.get_session().query(PeerClientKey) \
            .filter(PeerClientKey.client_id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return client

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

    def delete(self):
        try:
            Database.get_session().delete(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)
