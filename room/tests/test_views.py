import os
from django.urls import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from room.models import Room, Booking
import pytz
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") #nirla is the name of the project



class TestRoomFreeTimeView(TestCase):
    def setUp(self) -> None:

        self.client = APIClient()
        self.samarqand_vaqt = datetime.now()
        self.hozirgi_vaqt = self.samarqand_vaqt.strftime('%Y-%m-%d %H:%M:%S')
        self.kun_oxiri = self.samarqand_vaqt.date().strftime('%Y-%m-%d') + ' 23:59:59'
        self.room = Room.objects.create(name='express24', type='team', capacity=15)



    def test_get_today_free_time(self):

        url = reverse('availability', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('end'), self.kun_oxiri)
        self.assertEqual(response.data.get('start'), self.hozirgi_vaqt)


    def test_get_today_free_time_with_booking(self):
        self.hozir_add_hour = self.samarqand_vaqt + timedelta(hours=1)


        self.hozir_add_2hour = self.samarqand_vaqt + timedelta(hours=2)

        self.book = Booking.objects.create(room=self.room, resident='express', start=self.hozir_add_hour, end=self.hozir_add_2hour)
        url = reverse('availability', args=[self.room.id])
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('start'), self.hozirgi_vaqt)
        self.assertEqual(response.data[0].get('end'), self.hozir_add_hour)
        self.assertEqual(response.data[1].get('start'), self.hozir_add_2hour)
        self.assertEqual(response.data[1].get('end'), self.kun_oxiri)
        pass

