import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key123456789'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
