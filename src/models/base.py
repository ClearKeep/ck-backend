from flask_sqlalchemy import SQLAlchemy
from src.controllers import app

db = SQLAlchemy(app, session_options={'autocommit': True, 'autoflush': True})


class Database:
    __instance = None

    @staticmethod
    def get():
        if Database.__instance is None:
            Database.__instance = db
        return Database.__instance
