import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG = os.environ.get("DEBUG", "false")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "false")
SECRET_KEY = os.environ.get("SECRET_KEY")
PORT = int(os.environ.get("PORT", 5000))

def init_env_variables(app):
    global DEBUG
    global DATABASE_URL
    global SQLALCHEMY_TRACK_MODIFICATIONS
    global SECRET_KEY
    global PORT

    DEBUG = app.config['DEBUG']
    DATABASE_URL = app.config['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    SECRET_KEY = app.config['SECRET_KEY']
    PORT = app.config['PORT']

def get_env_variables():

    return {
        "DEBUG": DEBUG,
        "DATABASE_URL": DATABASE_URL,
        "SQLALCHEMY_TRACK_MODIFICATIONS": SQLALCHEMY_TRACK_MODIFICATIONS,
        "SECRET_KEY": SECRET_KEY,
        "PORT": PORT
    }
