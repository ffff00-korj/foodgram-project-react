from django.conf import settings


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
