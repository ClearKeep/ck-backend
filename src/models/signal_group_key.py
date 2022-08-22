from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import joinedload
from src.models.base import Database
from src.models.user import User
from src.models.notify_token import NotifyToken
from utils.logger import *

import logging
logger = logging.getLogger(__name__)
class GroupClientKey(Database.get().Model):
    __tablename__ = 'group_client_key'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    group_id = Database.get().Column(Database.get().Integer, nullable=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    client_workspace_domain = Database.get().Column(Database.get().String(255), nullable=True)
    client_workspace_group_id = Database.get().Column(Database.get().Integer, nullable=True)
    device_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    # client key for group
    client_key = Database.get().Column(Database.get().Binary, nullable=True)
    client_sender_key_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    client_sender_key = Database.get().Column(Database.get().Binary)
    client_public_key = Database.get().Column(Database.get().Binary)
    client_private_key = Database.get().Column(Database.get().String(1024), nullable=True)
    # end client key for group
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, group_id, client_id,
                client_workspace_domain=None,
                client_workspace_group_id=None,
                device_id=None,
                client_key=None,
                client_sender_key_id=None,
                client_sender_key=None,
                client_public_key=None,
                client_private_key=None):
        self.group_id = group_id
        self.client_workspace_domain = client_workspace_domain
        self.client_workspace_group_id = client_workspace_group_id
        self.client_id = client_id
        self.device_id = device_id
        # set client key
        self.client_key = client_key
        self.client_sender_key_id = client_sender_key_id
        self.client_sender_key = client_sender_key
        self.client_public_key = client_public_key
        self.client_private_key = client_private_key

        return self

    def add(self):
        client = self.get(self.group_id, self.client_id)
        if client is not None:
            self.id = client.id
            self.update()
            return self
        else:
            try:
                Database.get_session().add(self)
                Database.get_session().commit()
                return self
            except Exception as e:
                Database.get_session().rollback()
                logger.error(e, exc_info=True)

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
            .options(joinedload(User.tokens)) \
            .join(User, GroupClientKey.client_id == User.id, isouter=True) \
            .join(NotifyToken, User.id == NotifyToken.client_id) \
            .filter(GroupClientKey.group_id.in_(group_ids)) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.remove()
        return result

    def get_clients_in_group(self, group_id):
        result = Database.get_session().query(GroupClientKey, User) \
            .options(joinedload(User.tokens)) \
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
            logger.error(e, exc_info=True)

    def delete(self):
        try:
            Database.get_session().delete(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e, exc_info=True)

    def list_by_user_id_group_ids(self, client_id, group_ids):
        return Database.get_session().query(GroupClientKey) \
            .filter(GroupClientKey.client_id == client_id) \
            .filter(GroupClientKey.group_id.in_(group_ids)) \
            .all()

    def bulk_update(self, keys):
        try:
            for key in keys:
                Database.get_session().merge(key)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e, exc_info=True)
            raise
