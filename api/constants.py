from flask import Flask
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DUMMY_BOOKS = [
  {
    "id": 1,
    "title": "Things fall apart",
    "isbn": "1234567",
    "price": 30
  },
  {
    "id": 2,
    "title": "Man's Search for Meaning",
    "isbn": "12345677",
    "price": 40
  },
  {
    "id": 3,
    "title": "12 Rules for Life",
    "isbn": "1234567777",
    "price": 140
  }
]