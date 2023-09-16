import os
import pytest
import json
from api.helpers.user_helpers import get_token, authenticate
from api.constants import DUMMY_BOOKS

valid_user = {"firstname": "John", "lastname": "Doe", "email": "john.doe@test.com", "password": "1234567"}
secret_key = "testing"

@pytest.fixture(scope="function")
def app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///bookies_test.sqlite3")
    monkeypatch.setenv("SECRET_KEY", secret_key)

    from api.app import app
    from api.models.__utils import drop_db, init_db
    from api.models.__models import User

    init_db()

    # login users to get token
    user = User().add_user(
        _firstname=valid_user["firstname"],
        _lastname=valid_user["lastname"],
        _email=valid_user["email"],
        _password=valid_user["password"]
    )

    app.config["LOGIN_TOKEN"] = get_token(secret_key, user)

    yield app

    drop_db()

def test_create_book(app):
    book_data = DUMMY_BOOKS[1]
    response = app.test_client().post('/api/v1/books', json=book_data, headers={'Authorization': f'Bearer {app.config["LOGIN_TOKEN"]}'})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert data["book_data"]["title"].lower() == book_data["title"].lower()
    assert data["book_data"]["isbn"] == int(book_data["isbn"])
    assert data["success"] == True

def test_get_all_books(app):
    book_data = DUMMY_BOOKS[1]

    from api.models.__models import Book

    # get user Id from token
    user_id = authenticate(app.config["LOGIN_TOKEN"], secret_key=secret_key)["id"]
    # add book to db
    Book().add_book(
        _title=book_data["title"],
        _price=book_data["price"],
        _isbn=book_data["isbn"],
        _user_id=user_id,
        _image = ""
    )

    response = app.test_client().get('/api/v1/books', headers={'Authorization': f'Bearer {app.config["LOGIN_TOKEN"]}'})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data["book_data"][0]["title"].lower() == book_data["title"].lower()
    assert len(data["book_data"]) == 1
    assert data["success"] == True

def test_get_book_by_id(app):
    book_data = DUMMY_BOOKS[1]

    from api.models.__models import Book

    # get user Id from token
    user_id = authenticate(app.config["LOGIN_TOKEN"], secret_key=secret_key)["id"]
    # add book to db
    Book().add_book(
        _title=book_data["title"],
        _price=book_data["price"],
        _isbn=book_data["isbn"],
        _user_id=user_id,
        _image = ""
    )

    response = app.test_client().get('/api/v1/books/1', headers={'Authorization': f'Bearer {app.config["LOGIN_TOKEN"]}'})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data["book_data"]["title"].lower() == book_data["title"].lower()
    assert data["success"] == True

def test_fav_book(app):
    book_data = DUMMY_BOOKS[1]

    from api.models.__models import Book

    # get user Id from token
    user_id = authenticate(app.config["LOGIN_TOKEN"], secret_key=secret_key)["id"]
    # add book to db
    Book().add_book(
        _title=book_data["title"],
        _price=book_data["price"],
        _isbn=book_data["isbn"],
        _user_id=user_id,
        _image = ""
    )

    response = app.test_client().post('/api/v1/books/1/favourites', headers={'Authorization': f'Bearer {app.config["LOGIN_TOKEN"]}'})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data["book_data"]["favourite"] == True
    assert data["success"] == True
