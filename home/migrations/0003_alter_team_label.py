# Generated by Django 5.1.2 on 2025-04-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_team_image_alter_team_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='label',
            field=models.CharField(help_text='Die Verwendung der Jahreszahl und/oder Semester bietet sich an.', max_length=100, verbose_name='Bezeichnung'),
        ),
    ]
