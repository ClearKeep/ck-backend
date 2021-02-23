from src.models.base import Database


class ServerInfo(Database.get().Model):
    __tablename__ = 'server_info'
    id = Database.get().Column(Database.get().Integer, primary_key=True)
    stun_server = Database.get().Column(Database.get().String(500), nullable=True)
    turn_server = Database.get().Column(Database.get().String(500), nullable=True)

    def add(self):
        try:
            Database.get().session.add(self)
            Database.get().session.commit()
            return self
        except:
            Database.get().session.rollback()
            raise



    def get(self):
        server_info = self.query.one_or_none()
        Database.get().session.commit()
        return server_info

    def update(self):
        server_info = self.get()
        if server_info is not None:
            self.id = server_info.id
            try:
                Database.get().session.merge(self)
                Database.get().session.commit()
            except:
                Database.get().session.rollback()
                raise
        else:
            self.add()
        return True