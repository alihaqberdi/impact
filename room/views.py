from datetime import datetime
from .funcsion import get_next_day
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Room, Booking
from .serializers import RoomSerializers, DateTimeSerializer
from django.db.models import Q
import pytz
from .pagination import CustomPagination




class RoomsView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    pagination_class = CustomPagination
    # filter_backends =


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
        d = request.data
        room_obj = get_object_or_404(Room, pk=pk)
        res_name = d.get('resident')['name']
        start_time = datetime.strptime(request.data.get('start'), '%d-%m-%Y %H:%M:%S')
        end_time = datetime.strptime(request.data.get('end'), '%d-%m-%Y %H:%M:%S')
        if Booking.objects.filter(room__id=pk, start__lt=end_time, end__gt=start_time).exists():
            return Response({
                "error": "uzr, siz tanlagan vaqtda xona band"
            })
        Booking.objects.create(room=room_obj, resident_name=res_name, start=start_time, end=end_time)
        return Response({
            "message": "xona muvaffaqiyatli band qilindi"
        })


class RoomFreeTimeView(APIView):
    def get(self, request, room_id):
        roob_obj = get_object_or_404(Room, pk=room_id)

        samarqand_vaqt = pytz.timezone('Asia/Samarkand')
        hozirgi_vaqt = datetime.now(samarqand_vaqt)
        cheklov_vaqt = datetime.now(samarqand_vaqt).day
        filtering_vaqt = hozirgi_vaqt
        data_or_defaul = request.data
        end_day = f"{datetime.now().date().strftime('%d.%m.%Y')} 23:59:59"
        request_data = ''
        if data_or_defaul:
            serializer = DateTimeSerializer(data=data_or_defaul)
            if serializer.is_valid():
                request_data = request.data.get('date')
                end_day = f"{datetime.strptime(request_data, '%d.%m.%Y').strftime('%d.%m.%Y')} 23:59:59"
                filtering_vaqt = datetime.strptime(f"{request_data} 00:00:00", '%d.%m.%Y %H:%M:%S')
                cheklov_vaqt = get_next_day(request_data)
                book_obj = Booking.objects.filter(
                    Q(room=roob_obj, start__gte=filtering_vaqt, start__lte=cheklov_vaqt) | Q(room=roob_obj,
                                                                                             end__gte=filtering_vaqt)).order_by(
                    'start')
            else:
                return Response({'error': serializer.errors}, status=400)
        else:
            book_obj = Booking.objects.filter(room=roob_obj, start__gte=filtering_vaqt,
                                              start__day__lte=cheklov_vaqt).order_by()

        hozirgi_vaqt = hozirgi_vaqt.strftime('%d.%m.%Y %H:%M:%S')
        if len(book_obj) == 0:
            if request_data > hozirgi_vaqt:
                return Response({
                    "start": f"{filtering_vaqt.strftime('%d.%m.%Y')} 00:00:00",
                    "end": f"{datetime.strptime(request_data, '%d.%m.%Y').strftime('%d.%m.%Y')} 23:59:59"
                })
            return Response({
                "start": hozirgi_vaqt,
                "end": f"{datetime.now().date().strftime('%d.%m.%Y')} 23:59:59"
            }, )
        list_json = []
        obj_time = filtering_vaqt.strftime('%d.%m.%Y %H:%M:%S')
        for book in book_obj:
            b_start = book.start.strftime('%d.%m.%Y %H:%M:%S')
            if b_start > str(obj_time):
                list_json.append({
                    "start": obj_time,
                    "end": b_start
                })
            elif str(obj_time) < b_start:
                list_json.append(
                    {
                        "start": obj_time,
                        "end": b_start
                    }
                )
            obj_time = book.end.strftime('%d.%m.%Y %H:%M:%S')
        end_t = book.end.strftime('%d.%m.%Y %H:%M:%S')

        if end_t < end_day:
            list_json.append(
                {
                    "start": book.end.strftime('%d.%m.%Y %H:%M:%S'),
                    "end": end_day
                }
            )
        if list_json:
            return Response(list_json)
        return Response({"error": "uzr, siz tanlagan vaqtda xona band"})
