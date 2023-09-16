from api.helpers.book_helpers import validate_book, update_book, refine_book_data
from api.constants import DUMMY_BOOKS

def test_validate_book():
  book = {
    "title": "Things fall apart",
    "isbn": "1234567",
    "price": 30
  }

  res = validate_book(book=book, patch_check=True)
  assert res["is_valid"] == True

def test_update_book():
  book_to_update = DUMMY_BOOKS[1]
  book_update = { "title": "Love and Respect" }
  updated_book = update_book(book_to_update["id"], book_update, DUMMY_BOOKS) or {}

  assert updated_book["id"] == book_to_update["id"]
  assert updated_book["title"] == book_update["title"]

def test_refine_book_data():
  unrefined_book_data = { "title": "Love and Respect", "fake_key": "fake_value", "isbn": 12345, "price": 12 }
  refined_book = refine_book_data(unrefined_book_data) or {}

  assert refined_book["title"] == unrefined_book_data["title"]
  assert not hasattr(refined_book, "fake_key")
