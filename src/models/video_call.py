from datetime import datetime
from sqlalchemy.orm import relationship
from src.models.base import Database
from utils.logger import *
import logging
logger = logging.getLogger(__name__)
class VideoCall(Database.get().Model):
    __tablename__ = 'video_call'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    message_id = Database.get().Column(Database.get().String(36), unique=True)
    call_status = Database.get().Column(Database.get().String(36), nullable=True)
    call_type = Database.get().Column(Database.get().String(36), nullable=False)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    started_at = Database.get().Column(Database.get().DateTime, nullable=True)
    ended_at = Database.get().Column(Database.get().DateTime, nullable=True)

    def add(self):
        try:
            Database.get_session().add(self)
            Database.get_session().commit()
        except:
            Database.get_session().rollback()
            raise

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e, exc_info=True)

    def get(self, call_id):
        call = Database.get_session().query(VideoCall) \
            .filter(VideoCall.id == call_id) \
            .one_or_none()
        Database.get().session.remove()
        return call
