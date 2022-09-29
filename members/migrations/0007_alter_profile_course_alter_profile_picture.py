from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_profile_picture'),
    ]

    operations = [
        migrations.RenameModel('Profile', 'Member'),
        migrations.AlterField(
            model_name='member',
            name='course',
            field=models.CharField(choices=[
                ('EMO', 'E-Mobility'),
                ('IDE', 'Integrated Design Engineering'),
                ('ME', 'Mechanical Engineering'),
                ('MTC', 'Mechatronics'),
                ('SEM', 'Systems Engineering for Manufacturing'),
                ('IEL', 'Industrial Engineering / Logistics'),
                ('IEM', 'Industrial Engineering / Mechanical Engineering'),
            ], max_length=3),
        ),
        migrations.AlterField(
            model_name='member',
            name='picture',
            field=models.ImageField(upload_to=members.models.user_directory_path),
        ),
    ]
