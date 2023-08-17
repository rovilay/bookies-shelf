from flask import Response, json
from .constants import DUMMY_BOOKS

def validate_book(book, patch_check=False):
    # checks if book object contains all required properties
    book_keys = list(book.keys())
    valid_keys = ['title', 'isbn', 'price',
                  'image', 'image_name'] if patch_check else ['title', 'isbn', 'price']
    diff = set(valid_keys).intersection(book_keys) if patch_check else set(
        valid_keys).difference(book_keys)

    return {
        "is_valid": len(diff) > 0 if patch_check else len(diff) == 0,
        "missing_props": diff
    }

def get_all_books():
    response = Response(
        json.dumps({ "books": DUMMY_BOOKS }), status=200, mimetype='application/json')
    response.headers['Location'] = "/books"
    return response
