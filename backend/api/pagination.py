from rest_framework.pagination import PageNumberPagination


class LimitNumberPagination(PageNumberPagination):
    page_size = 6