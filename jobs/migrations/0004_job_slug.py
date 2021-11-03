from django.db import migrations, models
from django.utils.text import slugify


def set_unique_slug(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    for job in Job.objects.all():
        job.slug = slugify(job.title)
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_add_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.RunPython(set_unique_slug, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(unique=True),
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
    ]
