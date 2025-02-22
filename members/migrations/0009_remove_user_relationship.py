from django.db import migrations, models


def parse_details_from_user(apps, schema_editor) -> None:
    Member = apps.get_model("members", "Member")
    db_alias = schema_editor.connection.alias
    for member in Member.objects.using(db_alias).all():
        member.name = member.user.first_name
        member.email = member.user.email
        member.save()


def select_user_from_details(apps, schema_editor) -> None:
    Member = apps.get_model("members", "Member")
    User = apps.get_model("auth", "User")
    db_alias = schema_editor.connection.alias
    for member in Member.objects.using(db_alias).all():
        member.user = User.objects.using(db_alias).get(email=member.email)
        member.save()


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_alter_member_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(default='', help_text='First name should be enough', max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.EmailField(default='', help_text="Internal use only", verbose_name='Email address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='department',
            field=models.PositiveSmallIntegerField(choices=[
                (1, 'Administration'),
                (2, 'Finances'),
                (3, 'Public Relations'),
                (4, 'Studies & Science'),
                (5, 'Field Trips'),
                (6, 'Committee Work'),
                (7, 'Mentoring'),
                (8, 'Maintenance'),
                (9, 'Events'),
            ], default=1, verbose_name='Department'),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=parse_details_from_user,
            reverse_code=select_user_from_details,
        ),
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.RemoveField(
            model_name='member',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='member',
            name='jobs',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='biography',
            new_name='statement',
        ),
        migrations.AlterField(
            model_name='member',
            name='statement',
            field=models.CharField(blank=True, max_length=500, verbose_name='Statement'),
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(blank=True, help_text='Internal use only', null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='member',
            name='course',
            field=models.CharField(choices=[
                ('Bachelor', [
                    ('AI', 'AI Engineering'),
                    ('EMO', 'E-Mobility'),
                    ('ESC', 'Engineering Science'),
                    ('MB-B', 'Mechanical Engineering'),
                    ('MECH-B', 'Mechatronics'),
                    ('WLO', 'Industrial Engineering for Logistics'),
                    ('WMB', 'Industrial Engineering for Mechanical Engineering'),
                ]),
                ('Master',[
                    ('BE', 'Biomechanical Engineering'),
                    ('CME', 'Computational Methods in Engineering'),
                    ('IDE', 'Integrated Design Engineering'),
                    ('MB-M', 'Mechanical Engineering'),
                    ('MECH-M', 'Mechatronics'),
                    ('SEM', 'Systems Engineering for Manufacturing'),
                    ('WING', 'Industrial Engineering'),
                ])
            ], max_length=6, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='member',
            name='joined_at',
            field=models.DateField(help_text='Internal use only', verbose_name='Date of accession'),
        ),
        migrations.AlterField(
            model_name='member',
            name='picture',
            field=models.ImageField(upload_to='members/', verbose_name='Picture'),
        ),
    ]
