from django.core.exceptions import ValidationError
from django.db import models


class Excursion(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField('description', blank=True)
    date = models.DateField()
    seats = models.PositiveSmallIntegerField()
    is_car_required = models.BooleanField(default=True)
    registration_begins_at = models.DateTimeField(blank=True, null=True)
    registration_ends_at = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_seat_owners(self):
        return self.participant_set.order_by('created_on').all()[:self.seats]

    def get_waiting_list(self):
        return self.participant_set.order_by('created_on').all()[self.seats:]


def validate_university_email(value: str):
    username, host = value.split('@')
    if host not in ['ovgu.de', 'st.ovgu.de']:
        raise ValidationError("Es sind nur E-Mail-Adressen der Otto-von-Guericke-Universität Magdeburg erlaubt.",
                              code='email not in whitelist')


def validate_phone(value: str):
    if not value.startswith('+'):
        raise ValidationError("Deine Mobilnummer muss mit einer Ländervorwahl beginnen. (z.B. +49...)",
                              code='missing country code')


class Participant(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(validators=[validate_university_email])
    phone = models.CharField(max_length=16, validators=[validate_phone])
    is_car_owner = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_seat_owner(self):
        return self in self.excursion.get_seat_owners()
