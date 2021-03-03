from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Database:
    __instance = None

    @staticmethod
    def get():
        if Database.__instance is None:
            Database.__instance = db
        return Database.__instance

    @staticmethod
    def get_session():
        if Database.get().session is None:
            Database.get().session = Database.get().create_scoped_session()
        return Database.get().session



