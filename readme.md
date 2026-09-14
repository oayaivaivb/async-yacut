# 🔗 YaCut — сервис укорачивания ссылок

**YaCut** — backend-сервис для создания коротких ссылок с дополнительной возможностью асинхронной загрузки файлов на Яндекс Диск.

Проект реализует создание пользовательских и автоматически генерируемых коротких идентификаторов, REST API и асинхронное взаимодействие с внешним файловым сервисом.

## ✨ Основные возможности

* 🔗 Создание коротких ссылок с пользовательским или автоматически сгенерированным ID
* 📁 Асинхронная загрузка нескольких файлов на Яндекс Диск
* 🔄 Получение оригинальной ссылки по короткому идентификатору
* 📊 REST API для интеграции с другими сервисами
* 🗄️ Работа с SQLite / PostgreSQL
* 🧪 Автоматические тесты
* 🐳 Контейнеризация приложения через Docker
* 🌐 Развёртывание с использованием Nginx

## 🛠 Технологии

* **Python 3.12**
* **Flask 3.0.2**
* **SQLAlchemy 2.0.23**
* **Flask-Migrate**
* **aiohttp 3.10.3**
* **SQLite / PostgreSQL**
* **HTML / Bootstrap 4**
* **Docker / Nginx**

## 🚀 Запуск проекта

### Клонирование

```bash
git clone git@github.com:ваш-аккаунт/yacut.git
cd yacut
```

### Создание виртуального окружения

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token_here
```

### Миграции базы данных

```bash
flask db upgrade
```

### Запуск

```bash
flask run
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:5000/
```

## API

### Создание короткой ссылки

`POST /api/id/`

**Запрос:**

```json
{
  "url": "https://example.com/very-long-url",
  "custom_id": "my-short-link"
}
```

**Ответ:**

```json
{
  "url": "https://example.com/very-long-url",
  "short_link": "https://yacut.ru/my-short-link"
}
```

### Получение оригинальной ссылки

`GET /api/id/{short_id}/`

**Ответ:**

```json
{
  "url": "https://example.com/very-long-url"
}
```

## 📁 Структура проекта

```text
yacut/
├── yacut/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── api_views.py
│   ├── error_handlers.py
│   ├── id_generation.py
│   ├── yandexdisk.py
│   ├── templates/
│   └── static/
├── tests/
├── migrations/
├── requirements.txt
├── settings.py
└── README.md
```

