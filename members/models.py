from django.db import models
from django.utils.translation import gettext_lazy as _

def user_directory_path():
    pass


class Member(models.Model):
    # Add a data migration before changing these numbers
    ADMINISTRATION = 1
    FINANCES = 2
    PUBLIC_RELATIONS = 3
    STUDIES_AND_SCIENCE = 4
    FIELD_TRIPS = 5
    COMMITTEE_WORK = 6
    MENTORING = 7
    MAINTENANCE = 8
    EVENTS = 9

    DEPARTMENT_CHOICES = [
        (ADMINISTRATION, _("Administration")),          # Verwaltung
        (FINANCES, _("Finances")),                      # Finanzen
        (PUBLIC_RELATIONS, _("Public Relations")),      # Öffentlichkeitsarbeit
        (STUDIES_AND_SCIENCE, _("Studies & Science")),  # Studium & Lehre
        (FIELD_TRIPS, _("Field Trips")),                # Exkursionen
        (COMMITTEE_WORK, _("Committee Work")),          # Hochschulpolitik
        (MENTORING, _("Mentoring")),                    # Mentoring
        (MAINTENANCE, _("Maintenance")),                # Technik
        (EVENTS, _("Events")),                          # Veranstaltungen
    ]

    PROGRAM_CHOICES = {
        _("Bachelor"): {
            "AI": _("AI Engineering"),
            "EMO": _("E-Mobility"),
            "ESC": _("Engineering Science"),
            "MB-B": _("Mechanical Engineering (Bachelor)"),
            "MECH-B": _("Mechatronics (Bachelor)"),
            "WLO": _("Industrial Engineering for Logistics (Bachelor)"),
            "WMB": _("Industrial Engineering for Mechanical Engineering (Bachelor)"),
        },
        _("Master"): {
            "BE": _("Biomechanical Engineering"),
            "CME": _("Computational Methods in Engineering"),
            "IDE": _("Integrated Design Engineering"),
            "MB-M": _("Mechanical Engineering (Master)"),
            "MECH-M": _("Mechatronics (Master)"),
            "SEM": _("Systems Engineering for Manufacturing"),
            "WING": _("Industrial Engineering (Master)"),
        },
    }

    name = models.CharField(_("Name"), max_length=100, help_text="First name should be enough")
    email = models.EmailField(_("Email address"), help_text=_("Internal use only"))
    picture = models.ImageField(_("Picture"), upload_to="members/")
    statement = models.CharField(_("Statement"), max_length=500, blank=True)
    department = models.PositiveSmallIntegerField(_("Department"), choices=DEPARTMENT_CHOICES)
    program = models.CharField(_("Program"), max_length=6, choices=PROGRAM_CHOICES)
    birthday = models.DateField(_("Date of birth"), help_text=_("Internal use only"), blank=True, null=True)
    joined_at = models.DateField(_("Date of accession"))

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return str(self.name)
