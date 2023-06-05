from django.urls import path

from . import views
# Create your views here.
urlpatterns = [
    path('rooms/', views.RoomsView.as_view()),
    path('rooms/<int:pk>/', views.DetailRoom.as_view())
]