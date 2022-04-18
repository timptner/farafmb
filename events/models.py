from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    desc = models.TextField(_("Description"))
    registration_started_at = models.DateTimeField(_("Start of registration"), blank=True, null=True)
    registration_stopped_at = models.DateTimeField(_("Registration deadline"), blank=True, null=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        constraints = [
            models.CheckConstraint(check=models.Q(registration_stopped_at__gt=models.F('registration_started_at')),
                                   name='registration_period_valid'),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('events:info', kwargs={'pk': self.pk})

    def registration_status(self) -> str:
        if self.registration_stopped_at:
            if timezone.now() > self.registration_stopped_at:
                return 'closed'
        if self.registration_started_at:
            if timezone.now() < self.registration_started_at:
                return 'pending'
        return 'open'

    def registration_is_closed(self) -> bool:
        if self.registration_status() == 'open':
            return False
        return True


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,)
    first_name = models.CharField(_("First name"), max_length=200)
    last_name = models.CharField(_("Last name"), max_length=200)
    email = models.CharField(_("Email"), max_length=200)
    comment = models.TextField(_("Comment"), blank=True)
    registered_at = models.DateTimeField(_("Moment of registration"), auto_now_add=True)
    is_approved = models.BooleanField(_("Approval of registration"), default=False)

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        constraints = [
            models.UniqueConstraint(fields=('event', 'email'), name='unique_event_email_combination'),
        ]

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display_approval(self):
        return _("Approved participant") if self.is_approved else _("Rejected participant")

    def __str__(self) -> str:
        return self.full_name()
