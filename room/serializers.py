from rest_framework import serializers
from room.models import Room, Booking
from datetime import datetime, date





class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class DateTimeSerializer(serializers.Serializer):
    date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])

    def validate(self, attrs):
        value = attrs['date']
        # Perform validation logic here
        current_date = datetime.now()

        # Check if the date is in the past
        if str(value) < str(current_date):
            raise serializers.ValidationError("Kelgusi vaqtni kiriting")

        # Check if the date is beyond 2030
        if value.year > 2030:
            raise serializers.ValidationError("2030 yilgacha bo'lgan sana kiriting")

        # Return the validated value
        return value
