from crypt import methods
import os
from re import template
import sys
from pathlib import Path
current_file_path = Path(__file__).resolve()
sys.path.append(str(current_file_path.parent.parent.parent))
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

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
#from src.models.workspace import Workspace
from src.models.video_call import VideoCall
from src.models.note import Note
from src.models.authen_setting import AuthenSetting

db_config = get_system_config()['db']
db_connection = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
    user=db_config['username'],
    pw=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['name']
)

template_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'templates')
app = Flask(__name__, template_folder=template_dir)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 30
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300
app.config["SQLALCHEMY_MAX_OVERFLOW"] = -1

db.init_app(app)
migrate = Migrate(app, db)
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


@app.route('/deeplink', methods=['GET'])
def deeplink():
    forgot_password_deeplink = f"{get_system_config()['deeplink_scheme']}://"
    return render_template('deeplink.html', forgot_password_deeplink=forgot_password_deeplink)


@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Expose-Headers', 'Link')
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
