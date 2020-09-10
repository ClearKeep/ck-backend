from src.daos.base import BaseDAO
from src.models.user import User

class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    def getListUser(self):
        return self.model.query.all()

    def getUserByUsername(self, username):
        return self.model.query.filter_by(username=username).one_or_none()