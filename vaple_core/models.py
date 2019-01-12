from django.db import models


class Event(models.Model):
    SOUND_TYPES = (
        ('NONE', 'Keine'),
        ('SPCH', 'Sprache'),
        ('CNCT', 'Konzert'),
        ('MNTR', 'Konzert mit Monitor'),
    )
    title = models.CharField(max_length=512)
    room = models.CharField(max_length=512, default='')
    sound_type = models.CharField(
        max_length=8,
        choices=SOUND_TYPES,
        default='',
    )


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
