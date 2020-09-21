
class BaseService:
    def __init__(self, model):
        self.model = model

    def find_by_id(self, id):
        return self.model.query.filter_by(id=id).one_or_none()