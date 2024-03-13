from flask import Flask
from pymongo import MongoClient
from config.settings import Config

# Flask 애플리케이션 생성
app = Flask(__name__)
app.config.from_object(Config)


class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_database(self, db_name):
        return self.client[db_name]


mongo = MongoDB("mongodb+srv://admin:20020221@kweb.tuduaqz.mongodb.net/", "data")
db = mongo.get_database("data")
