from django.conf import settings
from django.db import models


class Event(models.Model):
    SOUND_TYPES = (
        ('NONE', 'Keine'),
        ('SPCH', 'Sprache'),
        ('CNCT', 'Konzert'),
        ('MNTR', 'Konzert mit Monitor'),
    )
    title = models.CharField(verbose_name='Titel', max_length=512)
    room = models.CharField(verbose_name='Raum', max_length=512, default='')
    sound_type = models.CharField(
        verbose_name='Beschallungsart',
        max_length=8,
        choices=SOUND_TYPES,
        default='',
    )
    ba = models.FilePathField(
        verbose_name='BA',
        path=settings.EVENTS_FOLDER,
        null=True,
        blank=True,
        recursive=True,
    )
    rider = models.FilePathField(
        verbose_name='Rider',
        null=True,
        blank=True,
        recursive=True,
        path=settings.EVENTS_FOLDER,
    )
    folder = models.FilePathField(
        verbose_name='Ordner',
        null=True,
        blank=True,
        recursive=True,
        path=settings.EVENTS_FOLDER,
        allow_files=False,
        allow_folders=True,
    )
    additional_info = models.TextField(
        verbose_name='Weitere informationen',
        null=True,
        blank=True,
    )


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
