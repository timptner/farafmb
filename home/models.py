from django.db import models


class Team(models.Model):
    label = models.CharField()
    image = models.ImageField(upload_to="teams/")
    release_date = models.DateField(unique=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self) -> str:
        return str(self.label)
