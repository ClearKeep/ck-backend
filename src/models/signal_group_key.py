from datetime import datetime
from sqlalchemy import ForeignKey
from src.models.base import Database
from src.models.user import User
from utils.logger import *


class GroupClientKey(Database.get().Model):
    __tablename__ = 'group_client_key'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    group_id = Database.get().Column(Database.get().Integer, nullable=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    client_workspace_domain = Database.get().Column(Database.get().String(255), nullable=True)
    client_workspace_group_id = Database.get().Column(Database.get().Integer, nullable=True)
    device_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    client_key = Database.get().Column(Database.get().Binary, nullable=True)
    identity_key_encrypted = Database.get().Column(Database.get().Binary)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, group_id, client_id, client_workspace_domain, client_workspace_group_id, device_id, client_key, identity_key_encrypted):
        self.group_id = group_id
        self.client_workspace_domain = client_workspace_domain
        self.client_workspace_group_id = client_workspace_group_id
        self.client_id = client_id
        self.device_id = device_id
        self.client_key = client_key
        self.identity_key_encrypted = identity_key_encrypted
        return self

    def add(self):
        client = self.get(self.group_id, self.client_id)
        if client is not None:
            return None
        else:
            try:
                Database.get_session().add(self)
                Database.get_session().commit()
                return self
            except Exception as e:
                Database.get_session().rollback()
                logger.error(e)

    def get(self, group_id, client_id):
        client = Database.get_session().query(GroupClientKey) \
            .filter(GroupClientKey.group_id == group_id, GroupClientKey.client_id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return client

    def get_all_in_group(self, group_id):
        client = Database.get_session().query(GroupClientKey) \
            .filter(GroupClientKey.group_id == group_id) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.remove()
        return client

    def get_clients_in_groups(self, group_ids):
        result = Database.get_session().query(GroupClientKey, User) \
            .join(User, GroupClientKey.client_id == User.id,  isouter=True) \
            .filter(GroupClientKey.group_id.in_(group_ids)) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.remove()
        return result

    def get_clients_in_group(self, group_id):
        result = Database.get_session().query(GroupClientKey, User) \
            .join(User, GroupClientKey.client_id == User.id, isouter=True) \
            .filter(GroupClientKey.group_id == group_id) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.remove()
        return result

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
