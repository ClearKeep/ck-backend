from datetime import datetime
import secrets
import json
from src.models.base import Database
from src.models.message import Message
from src.models.signal_group_key import GroupClientKey
from src.models.signal_peer_key import PeerClientKey
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from src.models.message_user_read import MessageUserRead
from utils.logger import *

import logging
logger = logging.getLogger(__name__)
class GroupChat(Database.get().Model):
    __tablename__ = 'group_chat'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    owner_group_id = Database.get().Column(Database.get().Integer, nullable=True)
    owner_workspace_domain = Database.get().Column(Database.get().String(255), nullable=True)
    group_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    group_avatar = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    group_type = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    group_clients = Database.get().Column(Database.get().Text, unique=False, nullable=True)
    group_rtc_token = Database.get().Column(Database.get().Text, unique=False, nullable=True)
    total_member = Database.get().Column(Database.get().Integer, nullable=True)
    created_by = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_by = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now, nullable=True)
    last_message_at = Database.get().Column(Database.get().DateTime, nullable=True)
    last_message_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    deleted_at = Database.get().Column(Database.get().DateTime, nullable=True)

    def add(self):
        try:
            Database.get_session().add(self)
            Database.get_session().commit()
            return self
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e, exc_info=True)

    def get(self, group_id):
        group = Database.get_session().query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.id == group_id) \
            .one_or_none()
        Database.get().session.remove()

        return group

    def get_group(self, group_id):
        group = Database.get_session().query(GroupChat) \
            .filter(GroupChat.id == group_id) \
            .one_or_none()
        Database.get().session.remove()
        return group

    def get_group_type(self, group_id):
        group = Database.get_session().query(GroupChat.group_type) \
            .filter(GroupChat.id == group_id) \
            .one_or_none()
        Database.get().session.remove()
        return group

    def search(self, keyword):
        search = "%{}%".format(keyword)
        group = Database.get_session().query(GroupChat, Message) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .filter(GroupChat.group_name.like(search)) \
            .all()
        Database.get().session.remove()
        return group

    def get_joined(self, client_id):
        result = Database.get_session().query(GroupChat, Message, GroupClientKey) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .join(Message, GroupChat.last_message_id == Message.id, isouter=True) \
            .options(joinedload(Message.users_read).joinedload(MessageUserRead.user)) \
            .filter(GroupClientKey.client_id == client_id) \
            .all()
        Database.get().session.remove()
        return result


    def get_joined_group_type(self, client_id, group_type):
        result = Database.get_session().query(GroupChat, GroupClientKey.id, GroupChat.group_clients) \
            .join(GroupClientKey, GroupChat.id == GroupClientKey.group_id) \
            .filter(GroupClientKey.client_id == client_id) \
            .filter(GroupChat.group_type == group_type) \
            .all()
        Database.get().session.remove()
        return result

    def get_by_group_owner(self, owner_group_id):
        result = Database.get_session().query(GroupChat) \
            .filter(GroupChat.owner_group_id == owner_group_id) \
            .all()
        Database.get().session.remove()
        return result

    def get_client_key_by_owner_group(self, group_id, client_id):
        client = Database.get_session().query(GroupClientKey) \
            .join(GroupChat, GroupClientKey.group_id == GroupChat.id, isouter=True) \
            .filter(GroupChat.owner_group_id == group_id, GroupClientKey.client_id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return client

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

    def get_group_rtc_token(self, group_id):
        result = Database.get_session().query(GroupChat.group_rtc_token) \
            .filter(GroupChat.id == group_id) \
            .first()
        Database.get().session.remove()
        return result

    def get_groups(self, group_ids, owner_group_ids):
        groups = Database.get_session().query(GroupChat) \
            .filter(or_(GroupChat.id.in_(group_ids), GroupChat.owner_group_id.in_(owner_group_ids))) \
            .all()
        Database.get().session.remove()
        return groups

    def is_owner_group(self):
        return not self.owner_group_id

    def delete_group_client_key_by_client_id(self, client_id):
        try:
            Database.get_session().query(GroupClientKey) \
                .filter(GroupClientKey.group_id == GroupChat.id) \
                .filter(GroupClientKey.client_id == client_id) \
                .filter(GroupChat.group_type == 'group') \
                .delete(synchronize_session=False)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            raise
    
    def delete_group_messages_by_client_id(self, client_id, group_id):
        try:
            Database.get_session().query(Message) \
                .filter(Message.group_id == group_id) \
                .filter(Message.from_client_id == client_id) \
                .delete()
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            raise

    def reset_group_client_key_by_client_id(self, client_id):
        try:
            Database.get_session().query(GroupClientKey) \
                .filter(GroupClientKey.group_id == GroupChat.id) \
                .filter(GroupClientKey.client_id == client_id) \
                .filter(GroupChat.group_type == 'group') \
                .update({
                    GroupClientKey.client_key: None,
                    GroupClientKey.client_private_key: None,
                    GroupClientKey.client_public_key: None,
                    GroupClientKey.client_sender_key: None,
                    GroupClientKey.client_sender_key_id: None,
                }, synchronize_session=False)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            raise

    def remove_client(self, client_id):
        clients = json.loads(self.group_clients)
        for client in clients:
            if client['id'] == client_id:
                clients.remove(client)
        self.group_clients = json.dumps(clients)
        self.total_member = len(clients)
        self.update()

    def __repr__(self):
        return '<GroupChat(id=%s, group_name=%s, owner_group_id=%s)>' % (self.id, self.group_name, self.owner_group_id)
