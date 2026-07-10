# YaCut — сервис укорачивания ссылок

[![Flask](https://img.shields.io/badge/Flask-3.0.2-000000?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-CC0000?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-3.10.3-2C5BB4?logo=aiohttp)](https://docs.aiohttp.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**YaCut** — это сервис для создания коротких ссылок с дополнительной функцией асинхронной загрузки файлов на Яндекс Диск.

---

## 📖 О проекте

YaCut позволяет:

- 🔗 **Сокращать ссылки** — создавать короткие ссылки с пользовательским или автоматически сгенерированным идентификатором.
- 📁 **Загружать файлы** — асинхронно загружать несколько файлов на Яндекс Диск и получать короткие ссылки для скачивания.
- 📊 **API** — REST API для интеграции с другими сервисами.

---

## 🛠️ Стек технологий

| Компонент | Технология |
|-----------|------------|
| **Бэкенд** | Python 3.12, Flask 3.0.2 |
| **База данных** | SQLAlchemy 2.0.23 (SQLite / PostgreSQL) |
| **Асинхронность** | aiohttp 3.10.3 |
| **Миграции** | Flask-Migrate |
| **Фронтенд** | HTML, Bootstrap 4 |
| **Деплой** | Docker, Nginx |

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория

```bash
git clone git@github.com:ваш-аккаунт/yacut.git
cd yacut
```

### 2. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# или
source venv/Scripts/activate   # Windows (Git Bash)
```

### 3. Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token_here
```

### 5. Создание базы данных и миграции

```bash
flask db upgrade
```

### 6. Запуск сервера

```bash
flask run
```



---

## 📁 Структура проекта

```
yacut/
├── yacut/                      # Основной пакет приложения
│   ├── __init__.py             # Инициализация Flask
│   ├── models.py               # Модели базы данных
│   ├── forms.py                # WTForms
│   ├── views.py                # Основные маршруты
│   ├── api_views.py            # API маршруты
│   ├── error_handlers.py       # Обработчики ошибок
│   ├── id_generation.py        # Генерация коротких ID
│   ├── yandexdisk.py           # Асинхронная работа с Яндекс Диском
│   ├── templates/              # HTML-шаблоны
│   └── static/                 # CSS, JS, изображения
├── tests/                      # Тесты
├── migrations/                 # Миграции БД
├── requirements.txt            # Зависимости
├── settings.py                 # Настройки
├── .env                        # Переменные окружения
└── README.md                   # Документация
```

---

## 🔗 API

### POST `/api/id/`

Создание короткой ссылки.

**Запрос:**
```json
{
  "url": "https://example.com/very-long-url",
  "custom_id": "my-short-link"
}
```

**Ответ (201):**
```json
{
  "url": "https://example.com/very-long-url",
  "short_link": "https://yacut.ru/my-short-link"
}
```

### GET `/api/id/{short_id}/`

Получение оригинальной ссылки.

**Ответ (200):**
```json
{
  "url": "https://example.com/very-long-url"
}
```

---

## 📌 Возможности

### Главная страница (`/`)

- Поле для длинной ссылки (обязательное)
- Поле для пользовательского короткого ID (опционально, ≤16 символов)
- Автогенерация ID из 6 символов (A-Z, a-z, 0-9)

### Страница загрузки файлов (`/files`)

- Загрузка нескольких файлов одновременно
- Асинхронная загрузка на Яндекс Диск
- Генерация коротких ссылок для каждого файла
- Отображение таблицы с результатами



