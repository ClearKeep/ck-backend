from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import joinedload
from src.models.base import Database
from src.models.user import User
from src.models.notify_token import NotifyToken
from utils.logger import *


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
            .join(NotifyToken, User.id == NotifyToken.client_id) \
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

    def update_bulk_client_key(self, client_id, list_group_client_key):
        try:
            for group_client_key in list_group_client_key:
                sql_update = 'UPDATE group_client_key SET ' \
                    'device_id=:device_id, ' \
                    'client_key=:client_key, ' \
                    'client_sender_key_id=:client_sender_key_id, ' \
                    'client_sender_key=:client_sender_key, ' \
                    'client_public_key=:client_public_key, ' \
                    'client_private_key=:client_private_key, ' \
                    'updated_at=NOW() ' \
                    'WHERE group_id=:group_id ' \
                    'AND client_id=:client_id'
                Database.get_session().execute(
                    sql_update,
                    {
                        'device_id': group_client_key.deviceId,
                        'client_key': group_client_key.clientKeyDistribution,
                        'client_sender_key_id': group_client_key.senderKeyId,
                        'client_sender_key': group_client_key.senderKey,
                        'client_public_key': group_client_key.publicKey,
                        'client_private_key': group_client_key.privateKey,
                        'group_id': group_client_key.groupId,
                        'client_id': client_id
                    }
                )
            Database.get_session().commit()
            return True
        except Exception as e:
            logger.error(e)
            Database.get_session().rollback()
            return False

    # def update_bulk_client_key_test(self, client_id, list_group_client_key):
    #     try:
    #         for group_client_key in list_group_client_key:
    #             sql_update = 'UPDATE group_client_key SET ' \
    #                 'device_id=:device_id, ' \
    #                 'updated_at=NOW() ' \
    #                 'WHERE group_id=:group_id ' \
    #                 'AND client_id=:client_id'
    #             Database.get_session().execute(
    #                 sql_update,
    #                 {
    #                     'device_id': group_client_key.deviceId,
    #                     'group_id': group_client_key.groupId,
    #                     'client_id': client_id
    #                 }
    #             )
    #         Database.get_session().commit()
    #         return True
    #     except Exception as e:
    #         logger.error(e)
    #         Database.get_session().rollback()
    #         return False


    def delete(self):
        try:
            Database.get_session().delete(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)
