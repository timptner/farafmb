# Generated by Django 3.2.4 on 2021-09-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_profile_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(upload_to=''),  # Changed to '' on 2022-09-29
        ),
    ]
