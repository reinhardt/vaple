# Generated by Django 2.1.5 on 2019-01-14 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaple_core', '0005_auto_20190114_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='additional_info',
            field=models.TextField(null=True, verbose_name='Weitere informationen'),
        ),
        migrations.AlterField(
            model_name='event',
            name='rider',
            field=models.FilePathField(blank=True, null=True, path='/home/reinhardt/projects/vaple/files', recursive=True, verbose_name='Rider'),
        ),
    ]
