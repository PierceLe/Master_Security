import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
)
from datetime import timedelta

from werkzeug.utils import secure_filename

from services import user_service

auth = Blueprint('auth', __name__, template_folder='routes')

UPLOAD_FOLDER_AVATAR = "static/images/avatars"
ALLOWED_EXTENSIONS_AVATAR = {"png", "jpg", "jpeg", "gif", "svg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_AVATAR


ACCESS_EXPIRES = timedelta(days=30)


@auth.route("/api/auth/salt", methods=["POST"])
def get_salt():
    username = request.json.get("username")
    salt = user_service.get_salt(username)
    if salt is None:
        return {"status_code": 400, "error": "user does not exist!"}, 400
    return {"status_code": 200, "data": {"salt": salt}}, 200


# handles a post request when the user clicks the log in button
@auth.route("/api/auth/login", methods=["POST"])
def login_user():
    username = request.json.get("username")
    hashed_password = request.json.get("password")
    user = user_service.get_user(username)
    if user is None:
        return {"status_code": 400, "error": "user does not exist!"}, 400

    if not (user.password == hashed_password):
        return {"status_code": 400, "error": "password does not match!"}, 400

    user_service.update_pbkey_by_id(user.user_id, request.json.get("pbKey"))
    access_token = create_access_token(identity=user.user_id, expires_delta=ACCESS_EXPIRES)
    json_response = jsonify({"status_code": 200, "data": {"username": username, "role": user.role}})
    set_access_cookies(json_response, access_token)
    return json_response, 200


# handles a post request when the user clicks the signup button
@auth.route("/api/auth/signup", methods=["POST"])
def signup_api():
    username = request.form.get("username")
    fullname = request.form.get("fullname")
    hashed_password = request.form.get("password")
    salt = request.form.get("salt")
    public_key = request.form.get("pb_key")
    avatar = UPLOAD_FOLDER_AVATAR + "/" + "default.svg"

    if "avatar" in request.files:
        file = request.files["avatar"]
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{username}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER_AVATAR, filename)
            file.save(file_path)
            avatar = file_path

    if user_service.get_user(username) is None:
        user_id = user_service.create(
            username=username,
            fullname=fullname,
            password=hashed_password,
            salt=salt,
            role="student",
            avatar=avatar,
            public_key=public_key
        )
        access_token = create_access_token(identity=user_id, expires_delta=ACCESS_EXPIRES)
        return jsonify({"status_code": 200, "data": {"username": username, "token": access_token}}), 200

    return jsonify({"status_code": 400, "error": "user already exists!"}), 400
