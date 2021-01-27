import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import db


class Server_info(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True)
    stun_server = db.Column(db.JSON, nullable=True)
    turn_server = db.Column(db.JSON, nullable=True)

    def get_info(self):
        server_info = self.query.one_or_none()
        return server_info