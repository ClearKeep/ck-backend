from flask import Flask
from utils.config import get_system_config
from src.controllers.turn_server import Server
# import asyncio
# import threading

# message_loop = asyncio.new_event_loop()
#
# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
# t = threading.Thread(target=start_loop,args=(message_loop,))
# t.start()

from src.models.base import db
import threading

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


# api = Api(app)
# api.add_resource(Server, '/turn-server')

@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Expose-Headers', 'Link')
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
