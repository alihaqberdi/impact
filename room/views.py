from datetime import datetime
from .funcsion import get_next_day
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Room, Booking
from .serializers import RoomSerializers, DateTimeSerializer
from django.db.models import Q
import pytz
from .pagination import CustomPagination
from django.contrib.postgres.search import TrigramSimilarity


class RoomsView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        room_obj = Room.objects.all()
        search_query = self.request.query_params.get('search')
        print(self.request)
        if search_query:
            room_obj = Room.objects.annotate(
                smilarity=TrigramSimilarity('name', search_query)).filter(smilarity__gt=0.3).order_by('-smilarity')

        return room_obj


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


class BookView(APIView):
    def post(self, request, pk):
        samarqand_vaqt = pytz.timezone('Asia/Samarkand')
        now = datetime.now(samarqand_vaqt)
        d = request.data
        room_obj = get_object_or_404(Room, pk=pk)
        res_name = d.get('resident')['name']
        try:
            start_time = datetime.strptime(request.data.get('start'), '%d-%m-%Y %H:%M:%S')
            end_time = datetime.strptime(request.data.get('end'), '%d-%m-%Y %H:%M:%S')
        except:
            return Response({
                "error": "Vaqtni to'g'ri kiriting"
            })

        if start_time > end_time:
            return Response({
                "error": "Vaqtni to'g'ri kiriting"
            })

        if str(start_time) < str(now):
            return Response({
                "error": "Kelgusi vaqtni  kiriting"
            })

        if Booking.objects.filter(room__id=pk, start__lt=end_time, end__gt=start_time).exists():
            return Response({
                "error": "uzr, siz tanlagan vaqtda xona band"
            })
        Booking.objects.create(room=room_obj, resident_name=res_name, start=start_time, end=end_time)
        return Response({
            "message": "xona muvaffaqiyatli band qilindi"
        })


          
        
