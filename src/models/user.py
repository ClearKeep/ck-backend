from src.models.base import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(100), unique=False, nullable=True)
    last_name = db.Column(db.String(100), unique=False, nullable=True)
    status = db.Column(db.String(256), unique=False, nullable=True)
    avatar = db.Column(db.String(256), unique=False, nullable=True)
    auth_source = db.Column(db.String(50), unique=False, nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Item(id=%s, username=%s, email=%s)>' % (self.id, self.username, self.email)
