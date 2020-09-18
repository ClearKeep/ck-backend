# import sqlalchemy as db
# from sqlalchemy.ext.declarative import declarative_base
from utils.config import get_system_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_config = get_system_config()['db']
db_connection = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
    user=db_config['username'],
    pw=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['name']
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
