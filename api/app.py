#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from .controllers.user import signup_user, login_user
from .controllers.book import get_all_books, get_books_by_id, create_books, modify_books, remove_books, fav_book, del_fav_book, get_all_fav_books
from .settings import PORT, SECRET_KEY, DEBUG, DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS
from .models.__utils import init_db

app = Flask(__name__)

app.config['DEBUG'] = DEBUG
app.config['DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

secret_key = app.config['SECRET_KEY']

url_prefix = '/api/v1'

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


@app.route(f'{url_prefix}/books')
def get_books():
    return get_all_books(secret_key)


@app.route(f'{url_prefix}/books/<int:id>')
def get_book(id):
    return get_books_by_id(secret_key, id)


@app.route(f'{url_prefix}/books', methods=['POST'])
def add_books():
    return create_books(secret_key)


@app.route(f'{url_prefix}/books/<int:id>', methods=['PUT', 'PATCH'])
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

if __name__ == '__main__':
    app.run(port=PORT)
