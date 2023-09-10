import json
from api.app import app, DUMMY_BOOKS

def test_get_all_books():
    response = app.test_client().get('/api/v1/books')
    books = json.loads(response.data.decode('utf-8')).get("books")

    assert response.status_code == 200
    assert type(books) is list
    assert len(books) is len(DUMMY_BOOKS)
    assert type(books[0]) is dict
    assert type(books[1]) is dict
    assert books[0]['title'] == DUMMY_BOOKS[0]['title']
    assert books[1]['title'] == DUMMY_BOOKS[1]['title']