import os


class Config(object):
    """Base configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DISK_TOKEN = os.environ.get('DISK_TOKEN')
