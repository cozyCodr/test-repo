from decouple import config
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = config('SECRET_KEY')
    OPENAI_API_KEY = config('OPENAI_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        'SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)


class DevConfig(Config):
    OPENAI_API_KEY = config('OPENAI_API_KEY')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'EduQuery.db')}"
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
