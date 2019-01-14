# Generated by Django 2.1.5 on 2019-01-14 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaple_core', '0003_event_sound_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ba',
            field=models.FilePathField(null=True, verbose_name='BA'),
        ),
        migrations.AddField(
            model_name='event',
            name='rider',
            field=models.FilePathField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='room',
            field=models.CharField(default='', max_length=512, verbose_name='Raum'),
        ),
        migrations.AlterField(
            model_name='event',
            name='sound_type',
            field=models.CharField(choices=[('NONE', 'Keine'), ('SPCH', 'Sprache'), ('CNCT', 'Konzert'), ('MNTR', 'Konzert mit Monitor')], default='', max_length=8, verbose_name='Beschallungsart'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=512, verbose_name='Titel'),
        ),
    ]
