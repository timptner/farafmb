from django.core.exceptions import ValidationError
from django.db import models


class Excursion(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField('description', blank=True)
    visit_on = models.DateTimeField()
    seats = models.PositiveSmallIntegerField()
    is_car_required = models.BooleanField(default=True)
    registration_begins_at = models.DateTimeField(blank=True, null=True)
    registration_ends_at = models.DateTimeField()


def validate_university_email(value: str):
    username, host = value.split('@')
    if host not in ['ovgu.de', 'st.ovgu.de']:
        raise ValidationError("Es sind nur E-Mail-Adressen der Otto-von-Guericke-Universität Magdeburg erlaubt.",
                              code='email not in whitelist')


def validate_phone(value: str):
    if not value.startswith('+'):
        raise ValidationError("Deine Mobilnummer muss mit einer Ländervorwahl beginnen. (z.B. +49...)",
                              code='missing country code')


class Participants(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(validators=[validate_university_email])
    phone = models.CharField(max_length=16, validators=[validate_phone])
    is_car_owner = models.BooleanField()
