from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import db


class Notify(db.Model):
    __tablename__ = 'notify'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), nullable=True)
    ref_client_id = db.Column(db.String(36), unique=False, nullable=True)
    ref_group_id = db.Column(db.Integer, unique=False, nullable=True)
    notify_type = db.Column(db.String(36), unique=False, nullable=True)  # new-peer, in-peer, new-group, in-group
    notify_image = db.Column(db.String(255), unique=False, nullable=True)
    notify_title = db.Column(db.String(255), unique=False, nullable=True)
    notify_content = db.Column(db.String(255), unique=False, nullable=True)
    notify_platform = db.Column(db.String(36), unique=False, nullable=True)
    read_flg = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_unread_notifies(self, client_id):
        notifies = self.query.filter_by(client_id=client_id, read_flg=False)
        return notifies

    def update(self):
        db.session.merge(self)
        db.session.commit()

