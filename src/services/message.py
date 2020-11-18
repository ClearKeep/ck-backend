from src.services.base import BaseService
from src.models.message import Message


class MessageService(BaseService):
    def __init__(self):
        super().__init__(Message())

    def add_message(self, group_id, from_client_id, message):
        self.model = Message(
            group_id=group_id,
            from_client_id=from_client_id,
            message=message,
        )
        new_message = self.model.add()
        return True


