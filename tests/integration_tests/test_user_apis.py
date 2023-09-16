import pytest
import json

valid_user = {"firstname": "John", "lastname": "Doe", "email": "john.doe@test.com", "password": "1234567"}

@pytest.fixture(scope="function")
def app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///bookies_test.sqlite3")
    monkeypatch.setenv("SECRET_KEY", "testing")

    from api.app import app
    from api.models.__utils import drop_db, init_db

    app.config.update({ "TESTING": True })

    init_db()

    yield app

    drop_db()


def test_register(app):
    response = app.test_client().post('/api/v1/register', json=valid_user)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert "token" in data
    assert data["success"] == True

def test_login(app):
    from api.models.__models import User

    # add user to DB
    User().add_user(
        _firstname=valid_user["firstname"],
        _lastname=valid_user["lastname"],
        _email=valid_user["email"],
        _password=valid_user["password"]
    )
    response = app.test_client().post('/api/v1/login', json=valid_user)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "token" in data
    assert data["success"] == True

