from api.app import validate_book

def test_validate_book():
  book = {
    "title": "Things fall apart",
    "isbn": "1234567",
    "price": 30
  }

  res = validate_book(book=book, patch_check=True)
  assert res["is_valid"] == True