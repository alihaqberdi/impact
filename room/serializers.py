from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from room.models import Room, Booking
from datetime import datetime, timedelta
import room.funcsion
import pytz


class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ResidentSerializer(serializers.Serializer):
    name = serializers.CharField()


class BookingSerializer(serializers.Serializer):
    resident = ResidentSerializer()
    start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    end = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    def validate(self, attrs):

        start_date = attrs.get('start')
        end_date = attrs.get('end')
        now = room.funcsion.time_converter(datetime.now() + timedelta(hours=5))

        if start_date < now:
            raise ValidationError("Kelgusi vaqtni  kiriting")

        if start_date > end_date:
            raise ValidationError("Vaqtni to'g'ri kiriting")

        if end_date.date() > start_date.date():
            raise ValidationError("Vaqtni to'g'ri kiriting")

        return attrs


class DateTimeSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

    def validate(self, attrs):
        value = attrs['date']
        current_date = datetime.now()

        if value < current_date.date():
            raise serializers.ValidationError("Kelgusi vaqtni kiriting")

        if value.year > 2023:
            raise serializers.ValidationError("2024 yilgacha bo'lgan sana kiriting")

        return attrs
