from datetime import datetime
from src.models.base import Database
from utils.logger import *


class Workspace(Database.get().Model):
    __tablename__ = 'workspace'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    workspace_domain = Database.get().Column(Database.get().String(255), nullable=True)
    is_default_workspace = Database.get().Column(Database.get().Boolean, nullable=True, default=False)
    is_own_workspace = Database.get().Column(Database.get().Boolean, nullable=True, default=False)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    deleted_at = Database.get().Column(Database.get().DateTime, nullable=True)

    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        # Database.get().session.remove()
        return self

    def get_joined_workspaces(self, client_id):
        message = Database.get_session().query(Workspace) \
            .filter(Workspace.client_id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return message

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
            # Database.get().session.remove()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)
