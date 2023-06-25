from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Room



class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                'page': self.page.number,
                'count': Room.objects.count(),
                'page_size': self.page_size,
                'results': data
            }
        )