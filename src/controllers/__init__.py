from flask import Flask
from utils.config import get_system_config
from src.controllers.turn_server import Server
from src.models.base import *
import threading

# need to import for create all table
from src.models.group import GroupChat
from src.models.message import Message
from src.models.notify import Notify
from src.models.notify_token import NotifyToken
from src.models.server_info import ServerInfo
from src.models.signal_group_key import GroupClientKey
from src.models.signal_peer_key import PeerClientKey
from src.models.user import User
from src.models.message_user_read import MessageUserRead

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
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 30
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300
app.config["SQLALCHEMY_MAX_OVERFLOW"] = -1

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/turn-server', methods=['GET'])
def turn_server():
    server = Server()
    return server.get()


@app.route('/thread', methods=['GET'])
def thread_server():
    response = {
        "total": threading.activeCount()
    }
    return response


@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Expose-Headers', 'Link')
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
