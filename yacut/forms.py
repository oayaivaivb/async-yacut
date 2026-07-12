from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    """Форма для создания сокращенной ссылки."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Отсутствует тело запроса'),
                    URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                min=1,
                max=16,
                message='Длина короткой ссылки не должна превышать 16 символов'
            ),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Короткая ссылка может содержать '
                'только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Сократить')


class FileForm(FlaskForm):
    """Форма для загрузки файла на Yandex Disk."""

    files = MultipleFileField(
        'Выберите файл для загрузки',
        validators=[DataRequired(message='Файл не выбран')]
    )
    submit = SubmitField('Загрузить')
