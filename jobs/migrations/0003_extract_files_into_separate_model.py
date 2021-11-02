import django.db.models.deletion
import jobs.models

from django.db import migrations, models
from django.utils.text import slugify


def set_unique_slug(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    for job in Job.objects.all():
        job.slug = slugify(job.title)
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_rename_description_job_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(editable=False, null=True),
        ),
        migrations.RunPython(set_unique_slug, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.RenameField(
            model_name='job',
            old_name='content',
            new_name='desc',
        ),
        migrations.AlterField(
            model_name='job',
            name='desc',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=jobs.models.job_directory_path)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
        ),
    ]
