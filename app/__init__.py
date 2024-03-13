from flask import Flask, jsonify
from config.settings import Config
from app.api import init_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    CORS(app, resources={r"/*": {"origins": "*"}})
    # 인증 API 블루프린트 등록
    init_app(app)

    return app
