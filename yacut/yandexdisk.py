import asyncio

import aiohttp

from . import app

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_TOKEN = app.config['DISK_TOKEN']

AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def upload_file_to_yandexdisk(file, session):
    """Загружает файл в выделенную папку приложения на Яндекс Диск."""
    if not file or not file.filename:
        raise ValueError('Файл не выбран или не имеет имени')

    filename = file.filename
    target_path = f'app:/{filename}'

    params = {
        'path': target_path,
        'overwrite': 'true'
    }

    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=params
    ) as response:
        if response.status != 200:
            error_text = await response.text()
            raise Exception(
                'Ошибка при получении URL загрузки: '
                f'{response.status}-{error_text}')

        data = await response.json()
        if 'href' not in data:
            error_msg = data.get('message', 'Неизвестная ошибка')
            raise Exception(
                f'Ошибка Yandex Disk API: {error_msg} (полный ответ: {data})')

        upload_url = data['href']

    file.seek(0)
    file_content = file.read()

    async with session.put(upload_url, data=file_content) as response:
        if response.status not in (201, 200):
            error_text = await response.text()
            raise Exception(f'Ошибка загрузки: {response.status}-{error_text}')
        return target_path


async def async_upload_files_to_yandexdisk(files):
    """Загружает несколько файлов на Яндекс Диск асинхронно."""
    if not files:
        return []

    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_file_to_yandexdisk(file, session)
            for file in files
        ]
        file_paths = await asyncio.gather(*tasks, return_exceptions=True)

        result = []
        for i, path in enumerate(file_paths):
            if isinstance(path, Exception):
                raise path
            result.append(path)

        return result


async def get_download_link(file_path, session):
    """Получает у API Яндекс Диска промежуточный URL для скачивания файла."""
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': file_path}
    ) as response:
        if response.status != 200:
            error_text = await response.text()
            raise Exception(
                'Ошибка при получении URL скачивания: '
                f'{response.status}-{error_text}')

        data = await response.json()
        if 'href' not in data:
            raise Exception(
                f'Ошибка URL скачивания: {data}')

        return data['href']
