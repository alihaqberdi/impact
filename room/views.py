from .funcsion import get_book_object
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Room, Booking
from .serializers import RoomSerializers, BookingSerializer
from .pagination import CustomPagination
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import status


class RoomsView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    pagination_class = CustomPagination  # Custom pagination  /pagination.py
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        room_obj = Room.objects.all()
        search_query = self.request.query_params.get('search')

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
                "error": "Xona Topilmadi"
            }, status.HTTP_404_NOT_FOUND)


class BookView(APIView):
    def post(self, request, pk):
        try:
            data = request.data
            Room.objects.get(pk=pk)
        except:
            return Response({
                "error": "Xona Topilmadi"
            })
        serializer = BookingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if Booking.objects.filter(room__id=pk, start__lt=serializer.data.get('end'),
                                      end__gt=serializer.data.get('start')).exists():
                return Response({
                    "error": "uzr, siz tanlagan vaqtda xona band"
                }, status.HTTP_400_BAD_REQUEST)
            valid_data = serializer.validated_data
            Booking.objects.create(
                room=Room.objects.get(pk=pk),
                start=valid_data.get('start'),
                end=valid_data.get('end'),
                resident=valid_data.get('resident').get('name'),

            )
            return Response({
                "message": "xona muvaffaqiyatli band qilindi"
            })



class RoomAvailability(APIView):


class RoomFreeTimeView2(APIView):

    def get(self, request, room_id):
        room_obj = get_object_or_404(Room, pk=room_id)
        data_or_defaul = (request.GET.get('date'))
        ans = get_book_object(room_obj, data_or_defaul)
        return Response(ans)

