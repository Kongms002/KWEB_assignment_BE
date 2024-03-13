from app.database.base import db

collection = db["user"]


def create_user(username, password, name, _id, grant):
    new_user = {
        "username": username,
        "password": password,
        "name": name,
        "_id": _id,
        "grant": grant,
        "course": [],
    }
    collection.insert_one(new_user)
    return new_user


def get_user_by_id(_id):
    return collection.find_one({"_id": _id})


def get_user_by_username(username):
    return collection.find_one({"username": username})


def get_all_users():
    return list(collection.find())


def delete_user(username):
    result = collection.delete_one({"username": username})
    return result.deleted_count > 0


def add_course_to_user(user_id, course_id):
    # 사용자 찾기
    user = collection.find_one({"_id": user_id})
    if user:
        # 사용자의 course 필드에 course_id 추가
        user["course"].append(course_id)
        # 업데이트된 사용자 정보를 저장
        collection.update_one({"_id": user_id}, {"$set": {"course": user["course"]}})
        return True
    else:
        return False
