from http import HTTPStatus
from flask import Blueprint, abort, jsonify, request, url_for
from flasgger import swag_from

from user.model.user import User, UserDetails
from app import db

user_api = Blueprint('user', __name__)


@user_api.route('/', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Create new user',
            'schema': 'Test'
        }
    }
})
def create_user():
    username = request.json.get('username')
    mail = request.json.get('mail')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')

    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    user = User(username=username, email=mail)
    user.set_password(password)
    user_details = UserDetails(firstname=firstname, lastname=lastname)
    user_details.user = user
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('user.get_user', id=user.id, _external=True)})


@user_api.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})
