from django.urls import path

from . import views
# Create your views here.
urlpatterns = [
    path('rooms/', views.RoomsView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.DetailRoom.as_view(), name='detail_room'),
    path('rooms/<int:pk>/book/', views.BookView.as_view(), name='booking'),
    path('rooms/<int:room_id>/availability/', views.RoomAvailability.as_view(), name='availability')
]