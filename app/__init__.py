import os 

from flask import Flask 
from configuration import BASE_DIR
from .models import db 
from flask_socketio import SocketIO

from app.main import main_blueprint
from app.api import api_blueprint

socketio = SocketIO(cors_allowed_origins='*')

def create_app(env_type: str):
    app = Flask(__name__)

    app.config.from_pyfile(os.path.join(BASE_DIR, 'configuration.py'))

    db.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)

    return app 

