from datetime import datetime, timedelta

from sqlalchemy.orm import relationship
from src.models.base import Database
from utils.logger import *


class AuthenSetting(Database.get().Model):
    __tablename__ = 'authen_setting'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    # hash_code setting
    hash_code_flow = Database.get().Column(
    # otp setting
    mfa_enable = Database.get().Column(Database.get().Boolean, unique=False, default=False)
    otp = Database.get().Column(Database.get().String(6), unique=False, nullable=True)
    otp_valid_time = Database.get().Column(Database.get().DateTime, unique=False, nullable=True)
    otp_changing_state = Database.get().Column(Database.get().INTEGER, unique=False, default=0)
    otp_tried_time = Database.get().Column(Database.get().INTEGER, unique=False, default=0)
    otp_request_counter = Database.get().Column(Database.get().INTEGER, unique=False, default=0)
    otp_frozen_time = Database.get().Column(Database.get().DateTime, unique=False, default=datetime.min)

    def add(self):
        try:
            Database.get_session().add(self)
            Database.get_session().commit()
            return self
        except:
            Database.get_session().rollback()
            raise

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

    def get(self, client_id):
        mfa_setting = Database.get_session().query(AuthenSetting) \
            .filter(AuthenSetting.id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return mfa_setting

    def __repr__(self):
        return '<Item(id=%s, mfa_enable=%s)>' % (self.id, self.mfa_enable)
