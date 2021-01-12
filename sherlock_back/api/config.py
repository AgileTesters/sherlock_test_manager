# -*- coding: utf8 -*-
"""Configuration params for sherlock."""
import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CORS_HEADER = 'Content-Type'
    TOKEN_TIMEOUT = 99999
    SECRET_KEY = secrets.token_urlsafe(20)
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
