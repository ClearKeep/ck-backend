
from src.models.base import Database


class BaseService:
    def __init__(self, model):
        self.model = model

    def find_by_id(self, id):
        result = self.model.query.filter_by(id=id).one_or_none()
        Database.get().session.commit()
        return result