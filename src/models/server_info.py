from src.models.base import db


class ServerInfo(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True)
    stun_server = db.Column(db.JSON, nullable=True)
    turn_server = db.Column(db.JSON, nullable=True)

    def get(self):
        server_info = self.query.one_or_none()
        return server_info

    def update(self):
        server_info = self.get()
        self.id = server_info.id
        db.session.merge(self)
        db.session.commit()
        return True