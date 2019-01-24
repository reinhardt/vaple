from django.conf import settings
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Event(models.Model):
    NONE = 'NONE'
    SPEECH = 'SPCH'
    CONCERT = 'CNCT'
    WITH_MONITOR = 'MNTR'
    SOUND_TYPES = (
        (NONE, 'Keine'),
        (SPEECH, 'Sprache'),
        (CONCERT, 'Konzert'),
        (WITH_MONITOR, 'Konzert mit Monitor'),
    )
    title = models.CharField(verbose_name='Titel', max_length=512)
    room = models.CharField(
        verbose_name='Raum',
        max_length=512,
        blank=True,
        default='',
    )
    sound_type = models.CharField(
        verbose_name='Beschallungsart',
        max_length=8,
        choices=SOUND_TYPES,
        default=NONE,
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

    def __str__(self):
        return self.title

    def fields_wanted(self):
        wanted = []
        if self.sound_type in [self.CONCERT, self.WITH_MONITOR]:
            if not self.rider:
                wanted.append('rider')
        return wanted


class EventDate(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    employees = models.ManyToManyField(
        Employee,
        verbose_name='Mitarbeiter',
        related_name='Veranstaltungstermin',
        blank=True,
    )

    def fields_wanted(self):
        wanted = []
        if (
                self.event.sound_type == Event.WITH_MONITOR and len(self.employees.values()) < 3 or
                self.event.sound_type == Event.CONCERT and len(self.employees.values()) < 2 or
                self.event.sound_type == Event.SPEECH and len(self.employees.values()) < 1
        ):
            wanted.append('employees')
        return wanted
