from src.services.base import BaseService
from src.models.user import User


class UserService(BaseService):
    def __init__(self):
        super().__init__(User())

    def create_new_user(self, id, email, username, auth_source):
        self.model = User(
            id=id,
            email=email,
            username=username,
            auth_source=auth_source
        )
        return self.model.add()

    # def get_list_user(self):
    #     return self.dao.get_list_user()

    # def get_user_by_username(self, username):
    #     return self.dao.get_user_by_username(username)
