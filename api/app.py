#!/usr/bin/env python3

from flask import Flask, Response, json
from .constants import DUMMY_BOOKS, PORT

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


app = Flask(__name__)

url_prefix = '/api/v1'

@app.route("/")
def welcome():
    return 'Hey bookie, Welcome!'

@app.route(f'{url_prefix}/')
def welcome_():
    return 'Hey bookie, Welcome!'

@app.route(f'{url_prefix}/books')
def get_books():
    return get_all_books()

if __name__ == '__main__':
    app.run(port=PORT)
