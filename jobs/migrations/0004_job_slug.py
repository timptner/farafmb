from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_add_document'),
    ]

    operations = [
        migrations.AddField(
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
