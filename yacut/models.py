from datetime import datetime

from . import db
from .constants import (MAX_ORIGINAL_NAME_LENGTH, MAX_PATH_LENGTH,
                        MAX_SHORT_ID_LENGTH)


class URLMap(db.Model):
    """Модель для хранения сопоставлений URL."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_NAME_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now)


class File(db.Model):
    """Модель для хранения загруженных файлов."""

    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(
        db.String(MAX_ORIGINAL_NAME_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH), unique=True, nullable=False)
    yandexdisk_path = db.Column(
        db.String(MAX_PATH_LENGTH), nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now)