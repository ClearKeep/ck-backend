from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import Database


class Notify(Database.get().Model):
    __tablename__ = 'notify'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    ref_client_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    ref_group_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    notify_type = Database.get().Column(Database.get().String(36), unique=False, nullable=True)  # new-peer, in-peer, new-group, in-group
    notify_image = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_title = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_content = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_platform = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    read_flg = Database.get().Column(Database.get().Boolean, nullable=True, default=False)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)

    def add(self):
        try:
            Database.get().session.add(self)
            Database.get().session.commit()
            return self
        except:
            Database.get().session.rollback()
            raise


    def get_unread_notifies(self, client_id):
        notifies = self.query.filter_by(client_id=client_id, read_flg=False)
        return notifies

    def update(self):
        try:
            Database.get().session.merge(self)
            Database.get().session.commit()
        except:
            Database.get().session.rollback()
            raise

