from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    suffix = filename.split(".")[-1].lower()
    return f"members/user_{instance.user.id}.{suffix}"


class Member(models.Model):
    EMO = "EMO"
    IDE = "IDE"
    ME = "ME"
    MTC = "MTC"
    SEM = "SEM"
    IEL = "IEL"
    IEM = "IEM"
    COURSES = [
        (EMO, _("E-Mobility")),
        (IDE, _("Integrated Design Engineering")),
        (ME, _("Mechanical Engineering")),
        (MTC, _("Mechatronics")),
        (SEM, _("Systems Engineering for Manufacturing")),
        (IEL, _("Industrial Engineering / Logistics")),
        (IEM, _("Industrial Engineering / Mechanical Engineering")),
    ]
    BSC = "BSC"
    MSC = "MSC"
    ABS = "ABS"
    DEGREES = [
        (BSC, _("Bachelor of Science")),
        (MSC, _("Master of Science")),
        (ABS, _("Alumnus")),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path)
    biography = models.CharField(max_length=250, blank=True)
    jobs = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=3, choices=COURSES)
    degree = models.CharField(max_length=3, choices=DEGREES)
    birthday = models.DateField(blank=True, null=True)
    joined_at = models.DateField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_degree_display_short(self):
        words = self.get_degree_display().split(" ")
        return words[0]

    def get_job_list(self):
        return [job.strip() for job in self.jobs.split(",")]

    def is_day_of_birth(self):
        if not self.birthday:
            return False
        today = timezone.now().date()
        return self.birthday.day == today.day and self.birthday.month == today.month
