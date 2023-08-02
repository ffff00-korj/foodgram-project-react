import base64
from typing import Union

from django.conf import settings
from django.core.files.base import ContentFile


def set_title_from_text(
    text: str,
    length: int = settings.MODEL_STR_REPRESENTATION_LIMIT,
) -> str:
    """Формирует заголовок из текста заданной длины.

    Args:
        text: текст, который будет использоваться как заголовок
        length: длина текста заголовка (без '...')

    Returns:
        возвращает текст + '...'
    """
    return text[:length] + '...' if len(text) > length else text


def base64_file(data: str, name: Union[str, None] = None) -> ContentFile:
    """Конвертирует base64-строку в файл.

    Args:
        data: base64-строка
        name: имя файла

    Returns:
        Файл, который можно сохранить в модель
    """
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name=f'{name}.{ext}')
