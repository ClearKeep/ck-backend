from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from utils.config import get_system_config

db_config = get_system_config()['db']
db_connection = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
    user=db_config['username'],
    pw=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['name']
)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 30
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300
app.config["SQLALCHEMY_MAX_OVERFLOW"] = -1

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


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
