import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .id_generation import get_unique_short_id
from .models import File, URLMap


@app.route('/api/id/', methods=['POST'])
def api_get_id():
    """API Эндпоинт для получения уникального короткого ID."""
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    original = data['url']
    custom_id = data.get('custom_id')
    if custom_id:
        custom_id = custom_id.strip()
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400)

        if not re.match(r'^[A-Za-z0-9]+$', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400)

        if (custom_id == 'files' or
                URLMap.query.filter_by(short=custom_id).first() or
                File.query.filter_by(short=custom_id).first()):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.', 400)

        short_id = custom_id
    else:
        short_id = get_unique_short_id()
        if short_id is None:
            raise InvalidAPIUsage(
                'Не удалось сгенерировать уникальный идентификатор', 500)
    new_url_map = URLMap(original=original, short=short_id)
    db.session.add(new_url_map)
    db.session.commit()
    short_link = url_for('redirect_view', short_id=short_id, _external=True)
    return jsonify({
        'url': original,
        'short_link': short_link
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def api_get_original(short_id):
    """API эндпоинт для получения оригинальной ссылки
    по короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
