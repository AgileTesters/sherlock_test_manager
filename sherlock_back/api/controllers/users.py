"""Sherlock User Controllers and Routes."""

from sherlock_back.api import db
from sherlock_back.api.data.model import User, UsersSchema


def find_user(**kwargs):
    user = User.query.filter_by(**kwargs).first()
    user_schema = UsersSchema(many=False)
    return user_schema.dump(user)


def get_all_users():
    user_schema = UsersSchema(many=True)
    users = user_schema.dump(User.query.all())
    return users


def create_user(name, email, password):
    """
    Param:
    {
        'name': required,
        'email': required - PrimaryKey,
        'password': required
     }
    """
    new_user = User(
        name=name,
        email=email,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()
    return True


def edit_user(user_id, edit_user_payload):
    # Check if email exist in the data base
    user_changes = dict(edit_user_payload)
    if user_changes.fetch('password', None):
        user_changes['password'] = User.generate_hash_password(user_changes['password'])

    userdata = User.query.filter(User.id == user_id).update(user_changes)
    db.session.add(userdata)
    db.session.commit()
    return True
