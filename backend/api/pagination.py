from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class RecipeLimitPagination(PageNumberPagination):
    page_size_query_param = 'recipes_limit'
