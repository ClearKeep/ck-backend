from datetime import datetime

from src.models.base import Database
from utils.config import get_system_config


class Message(Database.get().Model):
    __tablename__ = 'message'
    id = Database.get().Column(Database.get().String(36), primary_key=True)
    group_id = Database.get().Column(Database.get().Integer, nullable=True)
    from_client_id = Database.get().Column(Database.get().String(36), unique=False, nullable=True)
    client_id = Database.get().Column(Database.get().String(36), nullable=True)
    message = Database.get().Column(Database.get().Binary)
    created_at = Database.get().Column(Database.get().DateTime, default=datetime.now)
    updated_at = Database.get().Column(Database.get().DateTime, onupdate=datetime.now)
    deleted_at = Database.get().Column(Database.get().DateTime, nullable=True)

    def add(self):
        Database.get_session().add(self)
        Database.get_session().commit()
        return self

    def get_message_in_group(self, group_id, offset, from_time):
        result = Database.get_session().query(Message) \
            .filter(Message.group_id == group_id) \
            .all()
        Database.get().session.remove()
        # client = self.query.filter_by(group_id=group_id)
        #
        #
        # if from_time != 0:
        #     dt = datetime.fromtimestamp(from_time/1000) #from time in milisecond => second
        #     client = client.filter(Message.created_at > dt)
        #
        # client = client.order_by(Message.created_at.desc())
        #
        # if offset != 0:
        #     limit = get_system_config()['page_limit']
        #     client = client.offset(offset).limit(limit)
        #
        # result = client.all()
        return result

    def update(self):
        try:
            Database.get_session().merge(self)
            Database.get_session().commit()
        except:
            Database.get_session().rollback()
            raise
