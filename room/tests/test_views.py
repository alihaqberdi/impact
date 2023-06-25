from django.urls import reverse
from room.funcsion import RoomSerializers
from rest_framework.test import APIClient, APITestCase
from django.contrib.postgres.search import TrigramSimilarity
from room.models import Room, Booking
from datetime import datetime, timedelta
from rest_framework import status
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class TestRoomAvailabilityView(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.samarqand_vaqt = datetime.now() + timedelta(hours=5)
        self.samarqand_vaqt = datetime.strptime(self.samarqand_vaqt.strftime('%d-%m-%Y %H:%M:%S'), '%d-%m-%Y %H:%M:%S')
        self.hozirgi_vaqt = self.samarqand_vaqt.strftime('%d-%m-%Y %H:%M:%S')
        self.kun_oxiri = self.samarqand_vaqt.date().strftime('%d-%m-%Y') + ' 23:59:59'
        self.room = Room.objects.create(name='express24', type='team', capacity=15)
        self.hozir_add_hour = (self.samarqand_vaqt + timedelta(hours=1)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_2hour = (self.samarqand_vaqt + timedelta(hours=2)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_3hour = (self.samarqand_vaqt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_4hour = (self.samarqand_vaqt + timedelta(hours=4)).strftime('%d-%m-%Y %H:%M:%S')
        print(self.hozirgi_vaqt)
        print(self.kun_oxiri)
        print(self.hozir_add_hour)
        print(self.samarqand_vaqt)

    def test_free_time(self):
        url = reverse('availability', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('start'), self.hozirgi_vaqt)
        self.assertEqual(response.data[0].get('end'), self.kun_oxiri)

    # def test_with_booking(self):
    #     self.book = Booking.objects.create(room=self.room, resident='express', start=self.hozir_add_hour,
    #                                        end=self.hozir_add_2hour)
    #     url = reverse('availability', args=[self.room.id])
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data[0].get('start'), self.hozirgi_vaqt)
    #     self.assertEqual(response.data[0].get('end'), self.hozir_add_hour)
    #     self.assertEqual(response.data[1].get('start'), self.hozir_add_2hour)
    #     self.assertEqual(response.data[1].get('end'), self.kun_oxiri)

    # def test_parametr_date(self):
    #     self.book = Booking.objects.create(room=self.room, resident='express', start=self.hozir_add_hour,
    #                                        end=self.hozir_add_2hour)
    #     self.book2 = Booking.objects.create(room=self.room, resident='Google', start=self.hozir_add_3hour,
    #                                         end=self.hozir_add_4hour)
    #
    #     url = reverse('availability', args=[self.room.id])
    #     response = self.client.get(url, {'date': self.samarqand_vaqt.date()})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data[0].get('start'), self.hozirgi_vaqt)
    #     self.assertEqual(response.data[0].get('end'), self.hozir_add_hour)
    #     self.assertEqual(response.data[1].get('start'), self.hozir_add_2hour)
    #     self.assertEqual(response.data[1].get('end'), self.hozir_add_3hour)
    #     self.assertEqual(response.data[2].get('start'), self.hozir_add_4hour)
    #     self.assertEqual(response.data[2].get('end'), self.kun_oxiri)

    # def test_error_date(self):
    #     self.book = Booking.objects.create(room=self.room, resident='express', start=self.hozir_add_hour,
    #                                        end=self.hozir_add_2hour)
    #     url = reverse('availability', args=[self.room.id])
    #     now_minus_day = self.samarqand_vaqt - timedelta(days=1)
    #     response = self.client.get(url, {'date': now_minus_day.date()})
    #
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.data['error'][0], 'Kelgusi vaqtni kiriting')


class TestBookingView(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.room = Room.objects.create(name='express24', type='team', capacity=15)
        self.samarqand_vaqt = datetime.now() + timedelta(hours=5)
        self.samarqand_vaqt = datetime.strptime(self.samarqand_vaqt.strftime('%d-%m-%Y %H:%M:%S'), '%d-%m-%Y %H:%M:%S')
        self.hozir_add_hour = (self.samarqand_vaqt + timedelta(hours=1)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_2hour = (self.samarqand_vaqt + timedelta(hours=2)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_3hour = (self.samarqand_vaqt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M:%S')
        self.hozir_add_1day = (self.samarqand_vaqt + timedelta(days=1)).strftime('%d-%m-%Y %H:%M:%S')

    # def test_successful_booking(self):
    #     url = reverse('booking', args=[self.room.id])
    #     data = {
    #         'resident': {
    #             'name': 'Ali Haqberdiyev'
    #         },
    #         'start': self.hozir_add_hour,
    #         'end': self.hozir_add_2hour,
    #
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #
    #     booking = Booking.objects.get(room=self.room)
    #
    #     self.assertEqual(booking.resident, 'Ali Haqberdiyev')
    #     self.assertEqual(booking.start.strftime('%d-%m-%Y %H:%M:%S'), self.hozir_add_hour)
    #     self.assertEqual(booking.end.strftime('%d-%m-%Y %H:%M:%S'), self.hozir_add_2hour)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {
    #         'message': 'xona muvaffaqiyatli band qilindi'
    #     })

    # def test_band_vaqt(self):
    #     url = reverse('booking', args=[self.room.pk])
    #     booking_ali = Booking.objects.create(
    #         room=self.room,
    #         start=self.hozir_add_hour,
    #         end=self.hozir_add_2hour,
    #         resident='Ali'
    #     )
    #     data = {
    #         'resident': {
    #             'name': 'Alijon'
    #         },
    #         'start': self.hozir_add_hour,
    #         'end': self.hozir_add_3hour
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_410_GONE)
    #     self.assertEqual(response.data['error'],
    #                      "uzr, siz tanlagan vaqtda xona band"
    #                      )
    #
    # def test_error_date(self):
    #     url = reverse('booking', args=[self.room.pk])
    #     data = {
    #         'resident': {
    #             'name': 'Ali'
    #         },
    #         'start': self.hozir_add_3hour,
    #         'end': self.hozir_add_hour
    #     }
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'][0], 'Vaqtni to\'g\'ri kiriting')
    #
    #     data['start'] = self.hozir_add_3hour
    #     data['end'] = self.hozir_add_1day
    #
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'][0], "xonani 1-kundan ortiq band qilolmaysiz")


class TestDetailRoomView(APITestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Test Room", capacity=1, type='focus')

    def test_exists_room(self):
        url = reverse('detail_room', kwargs={'pk': self.room.pk})
        response = self.client.get(url)
        serializer = RoomSerializers(self.room)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_nonexistent_room(self):
        url = reverse('detail_room', kwargs={'pk': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'topilmadi'})


class TestRoomsView(APITestCase):
    def setUp(self):
        self.room1 = Room.objects.create(name="Xona 1", type="focus", capacity=1)
        self.room2 = Room.objects.create(name="Room 2", type="team", capacity=5)
        self.room3 = Room.objects.create(name="Room 3", type="conference", capacity=20)
        self.room4 = Room.objects.create(name="Room 4", type="team", capacity=5)

    def test_list_rooms(self):
        url = reverse('rooms')
        response = self.client.get(url)
        serializer = RoomSerializers(Room.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_create_room(self):
        url = reverse('rooms')
        data = {'name': 'New Room', 'type': 'team', 'capacity': '6'}
        response = self.client.post(url, data)
        room = Room.objects.get(name='New Room')
        serializer = RoomSerializers(room)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_filter_rooms_by_type(self):
        url = reverse('rooms') + '?type=team'
        response = self.client.get(url)
        serializer = RoomSerializers(Room.objects.filter(type='team'), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_search_rooms(self):
        url = reverse('rooms') + '?search=room'
        response = self.client.get(url)
        serializer = RoomSerializers(Room.objects.annotate(smilarity=TrigramSimilarity('name', 'room'))
                                     .filter(smilarity__gt=0.3).order_by('-smilarity'), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
