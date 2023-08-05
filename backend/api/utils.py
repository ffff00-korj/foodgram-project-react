from io import BytesIO

from django.http import FileResponse


def shopping_cart_representation_response(ingredients):
    result = ''
    for row in ingredients:
        result += (
            f'* {row.get("name")} '
            f'({row.get("measurement_unit")}) '
            f'- {row.get("amount")}\n'
        )

    return FileResponse(
        BytesIO(bytes(result, 'utf8')), filename='shopping_list.txt'
    )
