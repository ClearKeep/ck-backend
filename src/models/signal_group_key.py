from datetime import datetime

from sqlalchemy import ForeignKey

from src.models.base import Database
from src.models.user import User


class GroupClientKey(Database.get().Model):
    __tablename__ = 'group_client_key'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    group_id = Database.get().Column(Database.get().Integer, nullable=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    device_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    client_key = Database.get().Column(Database.get().Binary, nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, default=datetime.now, onupdate=datetime.now)

    def set_key(self, group_id, client_id, device_id, client_key):
        self.group_id = group_id
        self.client_id = client_id
        self.device_id = device_id
        self.client_key = client_key
        return self

    def add(self):
        client = self.get(self.group_id, self.client_id)
        if client is not None:
            self.id = client.id
            self.update()
        else:
            try:
                Database.get().session.add(self)
                Database.get().session.commit()
            except:
                Database.get().session.rollback()
                raise

    def get(self, group_id, client_id):
        client = self.query.filter_by(group_id=group_id, client_id=client_id).one_or_none()
        Database.get().session.commit()
        return client

    def get_all_in_group(self, group_id):
        client = self.query.filter_by(group_id=group_id) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.commit()
        return client

    def get_clients_in_groups(self, group_ids):
        result = Database.get().session.query(GroupClientKey.group_id, User) \
            .join(User, GroupClientKey.client_id == User.id) \
            .filter(GroupClientKey.group_id.in_(group_ids)) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.commit()
        return result

    def get_clients_in_group(self, group_id):
        result = Database.get().session.query(GroupClientKey.group_id, User) \
            .join(User, GroupClientKey.client_id == User.id) \
            .filter(GroupClientKey.group_id == group_id) \
            .order_by(GroupClientKey.client_id.asc()) \
            .all()
        Database.get().session.commit()
        return result

    # def get_clients_in_group_with_push_token(self, group_id):
    #     result = Database.get().session.query(GroupClientKey.group_id, User) \
    #         .join(User, GroupClientKey.client_id == User.id) \
    #         .filter(GroupClientKey.group_id == group_id) \
    #         .order_by(GroupClientKey.client_id.asc()) \
    #         .all()
    #     return result

    def update(self):
        try:
            Database.get().session.merge(self)
            Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise
