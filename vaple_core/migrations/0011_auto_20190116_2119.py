# Generated by Django 2.1.5 on 2019-01-16 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaple_core', '0010_auto_20190116_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='Veranstaltung', to='vaple_core.Employee', verbose_name='Mitarbeiter'),
        ),
    ]