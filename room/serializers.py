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
    name = serializers.CharField(required=False)


class BookingSerializer(serializers.Serializer):
    resident = ResidentSerializer()
    start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    end = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    def validate(self, attrs):

        start_date = attrs.get('start')
        end_date = attrs.get('end')
        now = room.funcsion.time_converter(datetime.now() + timedelta(hours=5))

        if start_date < now:
            raise ValidationError({"error": "Kelgusi vaqtni  kiriting"})

        if start_date >= end_date:
            raise ValidationError({"error": "Vaqtni to'g'ri kiriting"})

        if end_date.date() > start_date.date():
            raise ValidationError({'error': "xonani 1-kundan ortiq band qilolmaysiz"})

        if start_date > start_date + timedelta(days=30):
            raise ValidationError({"error": "xonani hozirgi vaqtdan 30 kungacha band qilish mumkin"})

        return attrs


class DateTimeSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

    def validate(self, attrs):
        value = attrs['date']
        current_date = datetime.now()

        if value < current_date.date():
            raise serializers.ValidationError({"error": "Kelgusi vaqtni kiriting"})

        if value > value + timedelta(days=30):
            raise serializers.ValidationError({"error": "30 kungacha bo'lgan sana kiriting"})

        return attrs
