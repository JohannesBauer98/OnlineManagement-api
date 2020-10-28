from http import HTTPStatus
from flask import Blueprint, abort, jsonify, request, url_for
from flask_login import current_user, login_user, logout_user

from user.model.user import User

import datetime

auth_api = Blueprint('auth', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        response_data = {
            "sucess": True,
            "status_code": 200,
        }
        return jsonify(response_data)
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        response_data = {
            "sucess": False,
            "status_code": 401,
        }
        return jsonify(response_data)
    login_user(user, True, datetime.timedelta(days=0,hours=1,minutes=0))
    response_data = {
        "sucess": True,
        "status_code": 200,
    }
    return jsonify(response_data)

@auth_api.route('/logout')
def logout():
    logout_user()
    response_data = {
        "sucess": True,
        "status_code": 200,
    }
    return jsonify(response_data)
