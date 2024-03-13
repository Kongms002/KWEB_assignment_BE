from flask import Blueprint, jsonify, request
from app.crud import crud_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    users = crud_user.get_all_users()
    return jsonify(users), 200


@user_bp.route("/users/<string:username>", methods=["GET"])
def get_user(username):
    user = crud_user.get_user_by_username(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404


# Add other endpoints such as user creation, update, and deletion here
