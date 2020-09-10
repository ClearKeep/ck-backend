from src.services.base import BaseService
from src.daos.user import UserDAO

class UserService(BaseService):
    def __init__(self):
        super().__init__(UserDAO())

    def getListUser(self):
        return self.dao.getListUser()

    def getUserByUsername(self, username):
        return self.dao.getUserByUsername(username)