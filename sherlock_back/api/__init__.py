"""Flask and plugin init"""
import pathlib


from flask import Flask, jsonify, make_response, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from sherlock_back.api.blueprints import register_blue_prints
from sherlock_back.api import config

app = Flask(__name__, instance_relative_config=True)
current_folder = pathlib.Path(__file__).parent.absolute()

app.config.from_object(config)


# TODO: https://github.com/AgileTesters/sherlock_test_manager/issues/29
from flask_cors import CORS
CORS(app, resources={r'/*': {"origins": '*', 'allow_headers': '*'}})
db_url = 'root:12345@127.0.0.1/sherlock'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}'.format(db_url)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = False


# Authentication Process
auth = HTTPTokenAuth(scheme='Bearer')
login = HTTPBasicAuth()


# Will load the Models and create the tables
db = SQLAlchemy(app)
from sherlock_back.api.data import model

register_blue_prints(app)


@auth.verify_token
def verify_token(user_token):
    user_data = model.User.verify_token_and_return_user(user_token)
    if user_data:
        g.user = user_data
        return True
    return False


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify(message="ENDPOINT_NOTFOUND"), 404)


@login.verify_password
def verify_password(email, password):
    user = model.User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        g.user = user
        return True
    return False


@app.route('/api/login', methods=['POST'])
@login.login_required
def login_and_generate_token():
    user_token = g.user.generate_auth_token(604800)
    return make_response(jsonify(
        {
            'token': user_token.decode('ascii'),
            'duration': 604800,
        })
    )
