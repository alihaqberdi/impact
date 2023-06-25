from datetime import datetime, timedelta
from room.serializers import DateTimeSerializer, RoomSerializers
from room.models import Booking

import pytz


def get_next_day(date):
    next_day = date + timedelta(days=1)
    next_day = datetime.strptime(next_day.strftime('%d-%m-%Y'), '%d-%m-%Y')
    return next_day


utc = pytz.UTC


def time_converter(time):
    return utc.localize(time)


def get_book_object(room_obj, date_or_default=None):
    now = time_converter(datetime.now() + timedelta(hours=5))
    filter_vaqt = now
    filter_cheklov_vaqt = get_next_day(now.date())
    if date_or_default:
        serializer = DateTimeSerializer(data={'date': date_or_default})
        if serializer.is_valid(raise_exception=True):
            date_or_default = datetime.strptime(date_or_default, '%d-%m-%Y')
            if date_or_default.date() > now.date():
                filter_vaqt = time_converter(date_or_default)
                filter_cheklov_vaqt = get_next_day(date_or_default.date())
    booking_objs = Booking.objects.filter(room=room_obj, start__gte=filter_vaqt, end__lt=filter_cheklov_vaqt)
    kun_boshi = filter_vaqt
    kun_oxiri = time_converter(datetime.strptime(f"{filter_vaqt.date().strftime('%d-%m-%Y')} 23:59:59", '%d-%m-%Y %H:%M:%S'))
    if len(booking_objs) == 0:
        return ({
            "start": kun_boshi.strftime("%d-%m-%Y %H:%M:%S"),
            "end": kun_oxiri.strftime("%d-%m-%Y %H:%M:%S")
        })
    list_availability = []
    for book in booking_objs:
        if book.start > kun_boshi:
            list_availability.append(
                {
                    'start': kun_boshi.strftime("%d-%m-%Y %H:%M:%S"),
                    'end': book.start.strftime("%d-%m-%Y %H:%M:%S"),
                }
            )
        kun_boshi = book.end
    if kun_oxiri > book.end:
        list_availability.append(
            {
                'start': book.end.strftime("%d-%m-%Y %H:%M:%S"),
                'end': kun_oxiri.strftime("%d-%m-%Y %H:%M:%S")
            }
        )
    if list_availability:
        return list_availability
    return {'error', "uzr, bu kunda xona band"}
