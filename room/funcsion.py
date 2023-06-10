from datetime import datetime, timedelta
from .serializers import DateTimeSerializer
from .models import Booking

import pytz


def get_next_day(date):
    next_day = date + timedelta(days=1)
    next_day = datetime.strptime(str(next_day), '%Y-%m-%d')
    return next_day


utc = pytz.UTC


def time_converter(time):
    return utc.localize(time)


def get_book_object(room_obj, data_or_defaul=None):
    now = datetime.now(pytz.timezone('Asia/Samarkand'))
    filter_vaqt = now
    filter_cheklov_vaqt = get_next_day(now.date())
    if data_or_defaul:
        serializer = DateTimeSerializer(data={'date': data_or_defaul})
        if serializer.is_valid(raise_exception=True):
            data_or_defaul = datetime.strptime(data_or_defaul, '%Y-%m-%d')
            if data_or_defaul.date() > now.date():
                filter_vaqt = time_converter(data_or_defaul)
                filter_cheklov_vaqt = get_next_day(data_or_defaul.date())
    booking_objs = Booking.objects.filter(room=room_obj, start__gte=filter_vaqt, end__lt=filter_cheklov_vaqt)
    print(booking_objs)
    kun_boshi = filter_vaqt
    kun_oxiri = time_converter(datetime.strptime(f"{filter_vaqt.date()} 23:59:59", '%Y-%m-%d %H:%M:%S'))
    if len(booking_objs) == 0:
        return ({
            "start": kun_boshi.strftime("%Y-%m-%d %H:%M:%S"),
            "end": kun_oxiri.strftime("%Y-%m-%d %H:%M:%S")
        })
    list_availability = []
    for book in booking_objs:
        if book.start > kun_boshi:
            list_availability.append(
                {
                    'start': kun_boshi.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': book.start.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        kun_boshi = book.end
    if kun_oxiri > book.end:
        list_availability.append(
            {
                'start': book.end.strftime("%Y-%m-%d %H:%M:%S"),
                'end': filter_cheklov_vaqt.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    if list_availability:
        return list_availability
    return {'error', '"uzr, siz tanlagan vaqtda xona band"'}
