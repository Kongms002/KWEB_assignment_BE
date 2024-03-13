from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.crud import crud_course, crud_post, crud_user
from datetime import datetime

course_bp = Blueprint("course", __name__)


@course_bp.route("/my_course_list", methods=["GET"])
@jwt_required()
def my_course_list():
    current_user_id = get_jwt_identity()
    user = crud_user.get_user_by_id(current_user_id)
    if user["grant"] == "admin":
        courses = crud_course.get_courses(writer_id=user["_id"])

    else:
        courses = crud_course.get_course_from_member(member_id=user["_id"])
    return jsonify(courses), 200


@course_bp.route("/my_post_list", methods=["GET"])
@jwt_required()
def get_all_posts_from_course():
    current_user_id = get_jwt_identity()
    user = crud_user.get_user_by_id(current_user_id)

    if user["grant"] == "admin":
        courses = crud_course.get_courses(writer_id=user["_id"])
    else:
        courses = crud_course.get_course_from_member(member_id=user["_id"])

    course_ids = [str(course["_id"]) for course in courses]

    posts = []
    # 해당 course의 post들을 가져와서 posts 배열에 추가합니다.
    for course_id in course_ids:
        posts.extend(crud_course.get_posts_from_course(course_id))

    return jsonify(posts), 200


@course_bp.route("/course_list", methods=["GET"])
@jwt_required()
def course_list():
    current_user_id = get_jwt_identity()
    user = crud_user.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "Permission denied"}), 403
    courses = crud_course.get_all_courses()
    return jsonify(courses), 200


@course_bp.route("/new", methods=["POST"])
@jwt_required()
def create_course():
    data = request.json
    name = data.get("name")
    _id = data.get("_id")
    current_user_id = get_jwt_identity()
    course = crud_course.get_course_by_id(_id)
    if course:
        return (
            jsonify({"message": "Course already registered"}),
            400,
        )
    new_course = crud_course.create_course(
        name=name, course_id=_id, writer_id=current_user_id
    )
    return (
        jsonify({"message": "New course created", "course_id": new_course["_id"]}),
        201,
    )


@course_bp.route("/<string:course_id>/get_members", methods=["GET"])
@jwt_required()
def get_members(course_id):
    current_user_id = get_jwt_identity()
    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404
    if course["writer_id"] != current_user_id:
        return jsonify({"message": "Permission denied"}), 403
    members = crud_course.get_members_from_course(course["_id"])
    return jsonify({"members": members}), 200


@course_bp.route("/<string:course_id>/get_posts", methods=["GET"])
@jwt_required()
def get_posts(course_id):
    current_user_id = get_jwt_identity()
    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404
    # if course["writer_id"] != current_user_id:
    #     return jsonify({"message": "Permission denied"}), 403
    posts = crud_course.get_posts_from_course(course["_id"])
    return jsonify({"posts": posts}), 200


@course_bp.route("/<string:course_id>/sugang", methods=["POST"])
@jwt_required()
def register_course(course_id):
    current_user_id = get_jwt_identity()
    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    user = crud_user.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if crud_course.get_member_from_course(course["_id"], current_user_id):
        return jsonify({"message": "User is already registered in this course"}), 400

    crud_course.add_member_to_course(course_id, user["_id"])
    return jsonify({"message": "User registered in course successfully"}), 200


@course_bp.route("/<string:course_id>/delete/<string:user_id>", methods=["DELETE"])
@jwt_required()
def delete_member(course_id, user_id):
    current_user_id = get_jwt_identity()
    current_user = crud_user.get_user_by_id(current_user_id)
    if current_user["grant"] != "admin":
        return jsonify({"message": "Permission denied"}), 403
    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404
    user_to_delete = crud_user.get_user_by_id(user_id)
    if not user_to_delete:
        return jsonify({"message": "User not found"}), 404
    if not crud_course.get_member_from_course(course["_id"], user_id):
        return jsonify({"message": "User is not registered in this course"}), 400
    if not crud_course.remove_member_from_course(course_id, user_id):
        return jsonify({"message": "Error occurd"}), 405
    return jsonify({"message": "User deleted from course successfully"}), 200


@course_bp.route("/<string:course_id>/cancel", methods=["DELETE"])
@jwt_required()
def cancel_course(course_id):
    user_id = get_jwt_identity()
    user = crud_user.get_user_by_id(user_id)

    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not crud_course.get_member_from_course(course_id, user_id):
        return jsonify({"message": "User is not registered in this course"}), 400

    if not crud_course.remove_member_from_course(course_id, user_id):
        return (
            jsonify({"message": "Error occurred while removing user from course"}),
            500,
        )

    return jsonify({"message": "User deleted from course successfully"}), 200


@course_bp.route("/<string:course_id>/new", methods=["POST"])
@jwt_required()
def create_post(course_id):
    current_user_id = get_jwt_identity()
    course = crud_course.get_course_by_id(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404
    if current_user_id != course["writer_id"]:
        return jsonify({"message": "Permission denied"}), 403
    data = request.json
    html_content = data.get("html_content")
    title = data.get("title")
    date = datetime.now()  # Assuming "post" is a relationship in the Course model
    new_post = crud_post.create_post(
        title=title, html=html_content, date=date, course_id=course_id
    )

    if not new_post:
        return jsonify({"message": "Error occured"}), 500
    return jsonify({"message": "New post created successfully"}), 201
