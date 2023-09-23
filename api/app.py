#!/usr/bin/env python3
import os
from flask import Flask, Response
from flask_cors import CORS
import prometheus_client
from .controllers.user_controller import signup_user, login_user, get_user
from .controllers.book_controller import get_all_books, get_books_by_id, create_books, modify_books, remove_books, fav_book, del_fav_book, get_all_fav_books
from .settings import init_env_variables
from .helpers.metrics import init_metrics

app = Flask(__name__)

app.config['DEBUG'] = os.environ.get("DEBUG", "false")
app.config['DATABASE_URL'] = os.environ.get("DATABASE_URL", "")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "false")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "")
app.config['PORT'] = int(os.environ.get("PORT", 5000))

secret_key = app.config['SECRET_KEY']

url_prefix = '/api/v1'

init_env_variables(app)
init_metrics(app)

from .models.__utils import init_db

init_db()

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route("/")
def welcome():
    return 'Hey bookie, Welcome!'

@app.route(f'{url_prefix}/')
def welcome_():
    return 'Hey bookie, Welcome!'

@app.route(f'{url_prefix}/register', methods=['POST'])
def signup():
    print('hello hello')
    return signup_user(secret_key)


@app.route(f'{url_prefix}/login', methods=['POST'])
def login():
    return login_user(secret_key)

@app.route(f'{url_prefix}/me', methods=['GET'])
def me():
    return get_user(secret_key)

@app.route(f'{url_prefix}/books')
def get_books():
    return get_all_books(secret_key)


@app.route(f'{url_prefix}/books/<int:id>')
def get_book(id):
    return get_books_by_id(secret_key, id)


@app.route(f'{url_prefix}/books', methods=['POST'])
def add_books():
    return create_books(secret_key)


@app.route(f'{url_prefix}/books/<int:id>', methods=['PUT'])
def update_books(id):
    return modify_books(secret_key, id)


@app.route(f'{url_prefix}/books/<int:id>', methods=['DELETE'])
def delete_books(id):
    return remove_books(secret_key, id)


@app.route(f'{url_prefix}/books/favourites')
def get_fav_books():
    return get_all_fav_books(secret_key)


@app.route(f'{url_prefix}/books/<int:id>/favourites', methods=['POST'])
def fav_books(id):
    return fav_book(secret_key, id)


@app.route(f'{url_prefix}/books/<int:id>/favourites', methods=['DELETE'])
def remove_fav_books(id):
    return del_fav_book(secret_key, id)

@app.route('/metrics/')
def metrics():
    return Response(prometheus_client.generate_latest())

if __name__ == '__main__':
    app.run(port=app.config['PORT'])
