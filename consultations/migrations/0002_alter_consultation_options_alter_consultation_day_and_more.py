# Generated by Django 4.0.2 on 2022-04-18 20:42

import consultations.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultation',
            options={'verbose_name': 'Consultation', 'verbose_name_plural': 'Consultations'},
        ),
        migrations.AlterField(
            model_name='consultation',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')], verbose_name='Day'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Visibility'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='member',
            field=models.CharField(max_length=50, verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='time',
            field=models.TimeField(verbose_name='Time'),
        ),
    ]
