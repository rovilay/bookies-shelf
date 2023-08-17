#!/usr/bin/env python3

from flask import Flask
from utils import BookUtils

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
    return BookUtils.get_all_books()
