"""Project config."""
import os
from os.path import abspath, dirname, join
from datetime import timedelta


class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = timedelta(seconds=300)
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_AUTH_HEADER_PREFIX = os.environ.get('JWT_AUTH_HEADER_PREFIX', 'FLASK')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):

    DEBUG = True
    PROJ_ROOT = dirname(dirname(abspath(__file__)))
    SQLITE_PATH = join(PROJ_ROOT, 'user.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_PATH}'


class ProductionConfig(Config):
    pass


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
