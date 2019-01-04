from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=512)
    room = models.CharField(max_length=512, default='')


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
