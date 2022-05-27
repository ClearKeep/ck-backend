from datetime import datetime
from src.models.base import Database
from utils.logger import *
import logging
logger = logging.getLogger(__name__)

class Notify(Database.get().Model):
    __tablename__ = 'notify'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    client_workspace_domain = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    ref_client_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    ref_group_id = Database.get().Column(Database.get().Integer, unique=False, nullable=True)
    ref_subject_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    ref_workspace_domain = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_type = Database.get().Column(Database.get().String(36), unique=False, nullable=True)  # new-peer, in-peer, new-group, in-group
    notify_image = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_title = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_content = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    notify_platform = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    read_flg = Database.get().Column(Database.get().Boolean, nullable=True, default=False)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)

    def add(self):
        try:
            Database.get_session().add(self)
            Database.get_session().commit()
            return self.get(self.id)
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

    def get(self, notify_id):
        notify = Database.get_session().query(Notify) \
            .filter(Notify.id == notify_id) \
            .one_or_none()
        Database.get().session.remove()
        return notify

    def get_unread_notifies(self, client_id):
        notifies = self.query.filter_by(client_id=client_id, read_flg=False)
        return notifies

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

