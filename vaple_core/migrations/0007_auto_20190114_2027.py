# Generated by Django 2.1.5 on 2019-01-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaple_core', '0006_auto_20190114_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='additional_info',
            field=models.TextField(blank=True, null=True, verbose_name='Weitere informationen'),
        ),
    ]