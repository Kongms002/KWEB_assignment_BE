from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.crud import crud_user
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify():
    current_user_id = get_jwt_identity()
    user = crud_user.get_user_by_id(current_user_id)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = crud_user.get_user_by_username(username)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user["_id"])
    return (
        jsonify(access_token=access_token),
        200,
    )


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    _id = data.get("_id")
    grant = data.get("grant")

    if not username or not password:
        return jsonify({"message": "Missing username, or password"}), 400

    existing_username = crud_user.get_user_by_username(username)
    if existing_username:
        return jsonify({"message": "Username already exists"}), 400
    existing_id = crud_user.get_user_by_id(_id)
    if existing_id:
        return jsonify({"message": "id already exists"}), 400
    hashed_password = generate_password_hash(password)
    new_user = crud_user.create_user(username, hashed_password, name, _id, grant)

    if not new_user:
        return jsonify({"message": "error occured"}), 500
    return (
        jsonify({"message": "User registered successfully"}),
        201,
    )
