import eventlet
import redis
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from .tetrisLogic import tetris_logic
from config import config

eventlet.monkey_patch()

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

tetris_logic.Shared.socket_out = SocketIO(message_queue='redis://127.0.0.1:6379/0')

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, message_queue='redis://127.0.0.1:6379/0', async_mode="eventlet")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
