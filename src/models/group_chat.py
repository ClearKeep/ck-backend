from src.models.base import db
from datetime import datetime


class GroupChat(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    group_name = db.Column(db.String(255), unique=False, nullable=True)
    created_by = db.Column(db.String(36), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.merge(self)
        db.session.commit()

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
