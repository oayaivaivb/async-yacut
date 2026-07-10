import random
import string

from .models import File, URLMap


def get_unique_short_id():
    """Generate a unique short ID for a URL mapping."""
    max_attempts = 50
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        short_id = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )
        if (URLMap.query.filter_by(short=short_id).first() is None and
                File.query.filter_by(short=short_id).first() is None):
            return short_id
    raise ValueError("Не удалось сгенерировать уникальный короткий ID")
