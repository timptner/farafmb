# Generated by Django 4.0.2 on 2022-02-19 23:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Exam', 'verbose_name_plural': 'Exams'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='course',
            field=models.CharField(max_length=150, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='date',
            field=models.DateField(verbose_name='Date of the exam'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='lecturer',
            field=models.CharField(max_length=100, verbose_name='Lecturer'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='minute_author',
            field=models.EmailField(max_length=254, null=True, verbose_name='Author of the minute'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='minute_file',
            field=models.FileField(upload_to='exams/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Minute file'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='submitted_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Submitted on'),
        ),
    ]
