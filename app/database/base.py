from flask import Flask
from pymongo import MongoClient

import os
from dotenv import load_dotenv


load_dotenv()

# Flask 애플리케이션 생성
app = Flask(__name__)

DB_URL = os.environ.get("DB_URL")


class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_database(self, db_name):
        return self.client[db_name]


mongo = MongoDB(DB_URL, "data")
db = mongo.get_database("data")
