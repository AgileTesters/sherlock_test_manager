"""Sherlock User Routes."""
from flask import Blueprint, request, jsonify, make_response, g

from sherlock_back.api import auth
from sherlock_back.api.controllers.users import get_all_users, find_user, create_user, edit_user
from sherlock_back.api.helpers.string_operations import safe_fetch_content

users = Blueprint('users', __name__)


# TODO: Deprecate this endpoint
@users.route('/get_all_users', methods=['GET'])
@auth.login_required
def all_users():
    return make_response(jsonify(get_all_users))


@users.route('/get_user_by_id/<int:user_id>', methods=['GET'])
@auth.login_required
def show_user_id(user_id):
    """Return a user.
    {
        "email": "email@email.com",
        "id": 1,
        "name": "Name"
    }
    """
    user = find_user(id=user_id)
    return make_response(jsonify(user))


@users.route('/get_user_by_email/<email>', methods=['GET'])
@auth.login_required
def show_user_email(email):
    user = find_user(email=email)
    return make_response(jsonify(user))


@users.route('/new', methods=['POST'])
def new_user():
    """
    Param:
    {
        'name': required,
        'email': required,
        'password': required
     }
    """

    # Avoid email duplicates - Better error Handler
    if find_user(email=safe_fetch_content(request, 'email')):
        return make_response(jsonify(message='EMAIL_IN_USE'))

    create_user(
        name=safe_fetch_content(request, 'name'),
        email=safe_fetch_content(request, 'email'),
        password=safe_fetch_content(request, 'password')
    )
    return make_response(jsonify(message='USER_CREATED'))


@users.route('/edit/<int:user_id>', methods=['POST'])
@auth.login_required
def edit(user_id):
    """
    Param:
    { user: (REQUIRED)
        {
            'name': not_required,
             'email': not_required,
             'password': not_required
        }
    }
    """
    if g.user.id != user_id:
        return make_response(jsonify(message='UNAUTHORIZED'), 401)

    # Avoid email duplicates - Better error Handler
    if find_user(email=safe_fetch_content(request, 'email')):
        return make_response(jsonify(message='EMAIL_IN_USE'))

    edit_user(user_id, request.get_json())
    return make_response(jsonify(message='USER_EDITED'))
