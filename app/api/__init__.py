from flask import Blueprint

from app.api.user import user_bp

from app.api.course import course_bp

# from app.api.post import post_bp
from app.api.auth import auth_bp


def init_app(app):
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(course_bp, url_prefix="/api/course")
    # app.register_blueprint(post_bp, url_prefix="/api/post")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
