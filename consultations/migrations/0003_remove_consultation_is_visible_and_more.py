# Generated by Django 4.1 on 2022-10-21 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_alter_consultation_options_alter_consultation_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='is_visible',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='member',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='time',
        ),
        migrations.AddField(
            model_name='consultation',
            name='end',
            field=models.TimeField(default=datetime.time(12, 0), verbose_name='End'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultation',
            name='start',
            field=models.TimeField(default=datetime.time(10, 0), verbose_name='Start'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultation',
            name='text',
            field=models.CharField(default='', max_length=50, verbose_name='Text'),
            preserve_default=False,
        ),
    ]
