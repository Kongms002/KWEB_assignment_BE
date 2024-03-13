from app.database.base import db
from app.crud import crud_user, crud_post

collection = db["course"]


def create_course(name, course_id, writer_id):

    course = {
        "_id": course_id,
        "name": name,
        "writer_id": writer_id,
        "posts_id": [],
        "members_id": [],
    }
    result = collection.insert_one(course)

    crud_user.add_course_to_user(writer_id, course_id)

    return course


def delete_course(course_id):
    result = collection.delete_one({"_id": course_id})
    return result.deleted_count > 0


def get_members_from_course(course_id):
    course = collection.find_one({"_id": course_id})
    if course:
        members_id = course.get("members_id", [])
        members = [crud_user.get_user_by_id(member_id) for member_id in members_id]
        return members
    return []


def get_all_courses():
    return list(collection)


def get_courses(writer_id):
    return list(collection.find({"writer_id": writer_id}))


def get_course_by_id(course_id):
    course = collection.find_one({"_id": course_id})
    return course


def get_member_from_course(course_id, user_id):
    course = collection.find_one({"_id": course_id})
    if course:
        members_id = course.get("members_id", [])
        if user_id in members_id:
            return True
    return False


def add_member_to_course(course_id, user_id):
    """
    MongoDB의 course 컬렉션에서 특정 코스에 사용자를 추가합니다.
    """
    # 코스를 찾습니다.
    course = collection.find_one({"_id": course_id})

    if course:
        # 코스의 members에 사용자 정보를 추가합니다.
        course["members_id"].append(user_id)
        # 업데이트된 코스를 저장합니다.
        collection.update_one(
            {"_id": course_id}, {"$set": {"members_id": course["members_id"]}}
        )
        return True
    else:
        return False


def remove_member_from_course(course_id, user_id):
    course = collection.find_one({"_id": course_id})

    if course:
        # 코스의 members에서 사용자를 제거합니다.
        if user_id in course["members_id"]:
            course["members_id"].remove(user_id)
            collection.update_one(
                {"_id": course_id}, {"$set": {"members_id": course["members_id"]}}
            )
            return True
        else:
            return False
    else:
        return False


def get_all_courses():
    return list(collection.find())


def get_course_from_member(member_id):
    courses = []
    for course in collection.find():
        if member_id in course["members_id"]:
            courses.append(course)
    return courses


def get_posts_from_course(course_id):
    course = collection.find_one({"_id": course_id})
    if course:
        posts_id = course.get("posts_id", [])
        posts = [crud_post.get_post_by_id(post_id) for post_id in posts_id]
        return posts
    return []


def add_post_to_course(course_id, post_id):

    course = collection.find_one({"_id": course_id})

    if course:
        course["posts_id"].append(post_id)
        # 업데이트된 코스를 저장합니다.
        collection.update_one(
            {"_id": course_id}, {"$set": {"posts_id": course["posts_id"]}}
        )
        return True
    else:
        return False
