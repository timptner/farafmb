# Generated by Django 3.2.4 on 2021-06-23 14:31

from django.db import migrations, models
import consultations.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=True)),
                ('member', models.CharField(max_length=50)),
                ('day', models.IntegerField(choices=[(1, 'Montag'), (2, 'Dienstag'), (3, 'Mittwoch'), (4, 'Donnerstag'), (5, 'Freitag')])),
                ('time', models.TimeField()),
            ],
        ),
    ]
