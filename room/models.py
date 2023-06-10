from django.db import models

# Create your models here.

class Room(models.Model):

    SELECT = (
        ('focus', 'Focus'),
        ('team', "Team"),
        ('conference', 'Conference')
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=30, choices=SELECT)
    capacity = models.PositiveIntegerField()


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    resident = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()


