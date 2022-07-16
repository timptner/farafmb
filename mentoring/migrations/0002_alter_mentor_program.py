# Generated by Django 4.0.5 on 2022-07-09 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentoring.program', verbose_name='Study program'),
        ),
    ]