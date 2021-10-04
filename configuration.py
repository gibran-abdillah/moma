import os
from sqlalchemy import create_engine



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_URI = os.getenv('DB_URI','sqlite:///{}'.format(os.path.join(BASE_DIR, 'database.db')))


SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SECRET_KEY = os.urandom(12)

