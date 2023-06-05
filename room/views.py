from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializers

class CustomPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        return Response(
            {
                'page': self.page.number,
                'count': len(self.page.object_list),
                'page_size': self.page_size,
                'result': data
            }
        )
class RoomsView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    pagination_class = CustomPagination


class DetailRoom(APIView):
    def get(self, request, pk):
        try:
            obj = Room.objects.get(pk=pk)
            objson = RoomSerializers(obj)
            return Response(objson.data)
        except:
            return Response({
                              "error": "topilmadi"
                            })
