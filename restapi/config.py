"""Project config."""
from os.path import abspath, dirname, join
from datetime import timedelta


class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = timedelta(seconds=300)
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
    SECRET_KEY = 'super-secret'


class TestingConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):

    DEBUG = True
    PROJ_ROOT = dirname(dirname(abspath(__file__)))
    SQLITE_PATH = join(PROJ_ROOT, 'dev.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_PATH}'


class ProductionConfig(Config):

    PROJ_ROOT = dirname(dirname(abspath(__file__)))
    SQLITE_PATH = join(PROJ_ROOT, 'prod.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_PATH}'


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
