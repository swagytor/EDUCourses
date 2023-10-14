from rest_framework.pagination import PageNumberPagination


class EducationPageNumberPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50
