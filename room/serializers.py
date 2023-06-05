from rest_framework.serializers import ModelSerializer
from room.models import Room



class RoomSerializers(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"



