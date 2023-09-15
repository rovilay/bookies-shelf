from flask import Flask
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DUMMY_BOOKS = [
  {
    "title": "Things fall apart",
    "isbn": "1234567",
    "price": 30
  },
  {
    "title": "Man's Search for Meaning",
    "isbn": "12345677",
    "price": 40
  },
  {
    "title": "12 Rules for Life",
    "isbn": "1234567777",
    "price": 140
  }
]