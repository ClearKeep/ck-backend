from src.models.base import Database
from datetime import datetime
from utils.logger import *

import logging
logger = logging.getLogger(__name__)
class ServerInfo(Database.get().Model):
    __tablename__ = 'server_info'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    stun_server = Database.get().Column(Database.get().String(500), nullable=True)
    turn_server = Database.get().Column(Database.get().String(500), nullable=True)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)

    def add(self):
        try:
            Database.get_session().add(self)
            Database.get_session().commit()
            return self
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e, exc_info=True)

    def get(self):
        server_info = Database.get_session().query(ServerInfo) \
            .filter(ServerInfo.id == 1) \
            .one_or_none()
        Database.get().session.remove()
        return server_info

    def update(self):
        server_info = self.get()
        if server_info is not None:
            self.id = server_info.id
            try:
                Database.get_session().merge(self)
                Database.get_session().commit()
            except Exception as e:
                Database.get_session().rollback()
                logger.error(e, exc_info=True)
        else:
            self.add()
        return True