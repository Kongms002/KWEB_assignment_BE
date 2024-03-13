from app.database.base import db
from app.crud import crud_course
from datetime import datetime

collection = db["post"]


def create_post(title, html, date, course_id):
    post_data = {"title": title, "html": html, "_id": date, "course_id": course_id}
    collection.insert_one(post_data)

    # 해당 강좌의 posts_id에 게시물의 _id 추가
    course = crud_course.get_course_by_id(course_id)
    if course:
        crud_course.add_post_to_course(course_id, post_data["_id"])

    return post_data


def delete_post(post_id):
    collection.delete_one({"_id": post_id})


def get_post_by_id(post_id):
    post = collection.find_one({"_id": post_id})
    return post
