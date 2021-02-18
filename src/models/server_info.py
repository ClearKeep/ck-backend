from src.models.base import db


class ServerInfo(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True)
    stun_server = db.Column(db.String(500), nullable=True)
    turn_server = db.Column(db.String(500), nullable=True)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            raise



    def get(self):
        server_info = self.query.one_or_none()
        return server_info

    def update(self):
        server_info = self.get()
        if server_info is not None:
            self.id = server_info.id
            try:
                db.session.merge(self)
                db.session.commit()
            except:
                db.session.rollback()
                raise
        else:
            self.add()
        return True