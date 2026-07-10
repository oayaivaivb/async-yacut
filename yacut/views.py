import urllib.parse

import aiohttp
from flask import Response, abort, flash, redirect, render_template

from . import app, db
from .forms import FileForm, URLMapForm
from .id_generation import get_unique_short_id
from .models import File, URLMap
from .yandexdisk import (AUTH_HEADERS, async_upload_files_to_yandexdisk,
                         get_download_link)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Рендерит главную страницу."""
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            short_id = custom_id.strip()

            if (short_id == 'files' or
                    URLMap.query.filter_by(short=short_id).first() or
                    File.query.filter_by(short=short_id).first()):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()
            if short_id is None:
                flash('Не удалось сгенерировать уникальный идентификатор')
                return render_template('index.html', form=form)

        new_url_map = URLMap(original=original_link, short=short_id)
        db.session.add(new_url_map)
        db.session.commit()

        return render_template('index.html', form=form, short_id=short_id)

    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    """Рендерит страницу загрузки файлов с оптимизированными запросами."""
    form = FileForm()
    uploaded_files = []

    if form.validate_on_submit():
        file_data = form.files.data
        file_paths = await async_upload_files_to_yandexdisk(file_data)

        async with aiohttp.ClientSession() as session:
            for file, file_path in zip(file_data, file_paths):
                short_id = get_unique_short_id()
                if short_id is None:
                    flash('Не удалось сгенерировать уникальный идентификатор')
                    return render_template(
                        'files.html', form=form, uploaded_files=uploaded_files)

                await get_download_link(file_path, session)

                new_file = File(
                    original_name=file.filename,
                    short=short_id,
                    yandexdisk_path=file_path
                )
                db.session.add(new_file)
                uploaded_files.append(new_file)

        db.session.commit()
        return render_template(
            'files.html', form=form, uploaded_files=uploaded_files)

    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files)


@app.route('/<short_id>')
async def redirect_view(short_id):
    """Редирект на оригинальный URL или прокси поток файла Yandex Disk ."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map:
        return redirect(url_map.original)

    file_entry = File.query.filter_by(short=short_id).first()
    if file_entry:
        async with aiohttp.ClientSession() as session:
            download_url = await get_download_link(
                file_entry.yandexdisk_path, session)

            async with session.get(
                    download_url, headers=AUTH_HEADERS) as response:
                if response.status != 200:
                    abort(response.status)

                file_bytes = await response.read()
                safe_filename = urllib.parse.quote(file_entry.original_name)
                return Response(
                    file_bytes,
                    headers={
                        'Content-Type': response.headers.get('Content-Type', 'application/octet-stream'),
                        'Content-Disposition': f"attachment; filename*=UTF-8''{safe_filename}"
                    }
                )
    abort(404)
