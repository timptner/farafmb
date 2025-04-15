from django.db import models


class Team(models.Model):
    label = models.CharField(
        verbose_name="Bezeichnung",
        max_length=100,
        help_text="Die Verwendung der Jahreszahl und/oder Semester bietet sich an.",
    )
    image = models.ImageField(
        verbose_name="Bild",
        help_text="Bild mit den aktuellen Mitgliedern",
        upload_to="teams/",
    )
    release_date = models.DateField(
        verbose_name="Freigabedatum",
        help_text="Datum der Veröffentlichung",
        unique=True,
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self) -> str:
        return str(self.label)
