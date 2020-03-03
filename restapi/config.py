"""Project config."""
import os
from os.path import abspath, dirname, join
from datetime import timedelta


class Config:

    PROJ_ROOT = dirname(dirname(abspath(__file__)))
    SQLITE_PATH = join(PROJ_ROOT, 'user.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{SQLITE_PATH}')  # noqa: E501
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret'
    JWT_EXPIRATION_DELTA = timedelta(seconds=300)
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_AUTH_HEADER_PREFIX = 'FLASK'
