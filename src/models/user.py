from datetime import datetime
from sqlalchemy.orm import relationship
from src.models.base import Database
from utils.logger import *


class User(Database.get().Model):
    __tablename__ = 'user'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    iv_parameter = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    email = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    password_verifier = Database.get().Column(Database.get().String(2048), unique=False, nullable=True)
    salt = Database.get().Column(Database.get().String(512), unique=False, nullable=True)
    srp_server_private = Database.get().Column(Database.get().String(2048), unique=False, nullable=True)
    display_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    first_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    last_name = Database.get().Column(Database.get().String(255), unique=False, nullable=True)
    status = Database.get().Column(Database.get().String(256), unique=False, nullable=True)
    avatar = Database.get().Column(Database.get().String(256), unique=False, nullable=True)
    phone_number = Database.get().Column(Database.get().String(20), unique=False, nullable=True)
    auth_source = Database.get().Column(Database.get().String(50), unique=False, nullable=True)
    active = Database.get().Column(Database.get().Boolean, unique=False, nullable=True, default=True)
    last_active_at = Database.get().Column(Database.get().DateTime, nullable=True)
    last_login_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    tokens = relationship('NotifyToken', back_populates='user', cascade="delete")
    messages_read = relationship('MessageUserRead', back_populates='user', cascade="delete")

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
            logger.error(e)

    def get(self, client_id):
        user = Database.get_session().query(User) \
            .filter(User.id == client_id) \
            .one_or_none()
        Database.get().session.remove()
        return user

    def get_user_by_auth_source(self, email, auth_source):
        user = Database.get_session().query(User) \
            .filter(User.email == email) \
            .filter(User.auth_source == auth_source) \
            .one_or_none()
        Database.get().session.remove()
        return user

    def get_google_user(self, email, auth_source):
        user = Database.get_session().query(User) \
            .filter(User.email == email) \
            .filter(User.auth_source == auth_source) \
            .one_or_none()
        Database.get().session.remove()
        return user

    def search(self, keyword, client_id):
        search = "%{}%".format(keyword)
        user = Database.get_session().query(User) \
            .filter(User.id != client_id) \
            .filter(User.display_name.ilike(search)) \
            .filter(User.last_login_at != None) \
            .all()
        Database.get().session.remove()
        return user

    def get_users(self, client_id):
        user = Database.get_session().query(User) \
            .filter(User.id != client_id) \
            .filter(User.last_login_at != None) \
            .all()
        Database.get().session.remove()
        return user

    def get_client_id_with_push_token(self, id):
        result = Database.get_session().query(User.id, User) \
            .filter(User.id == id) \
            .first()
        Database.get().session.remove()
        return result

    def delete(self):
        try:
            Database.get_session().delete(self)
            Database.get_session().commit()
        except Exception as e:
            Database.get_session().rollback()
            logger.error(e)

    def __repr__(self):
        return '<Item(id=%s, display_name=%s, email=%s)>' % (self.id, self.display_name, self.email)
