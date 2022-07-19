import csv

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView

from .forms import RegistrationForm, ProgramForm, MentorForm
from .models import Registration, Program, Mentor


class RegistrationListView(LoginRequiredMixin, ListView):
    model = Registration


class RegistrationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    success_url = reverse_lazy('mentoring:registration-list')
    success_message = _("%(name)s was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_list'] = Registration.objects.all()
        return context


class RegistrationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Registration
    success_url = reverse_lazy('mentoring:registration-list')
    success_message = _("Registration was deleted successfully")


class ProgramListView(LoginRequiredMixin, ListView):
    model = Program


class ProgramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Program
    form_class = ProgramForm
    success_url = reverse_lazy('mentoring:program-list')
    success_message = _("%(name)s was created successfully")


class ProgramDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Program
    success_url = reverse_lazy('mentoring:program-list')
    success_message = _("Program was deleted successfully")


class MentorListView(LoginRequiredMixin, ListView):
    template_name = 'mentoring/mentor_list.html'
    model = Mentor


@login_required
def export_as_csv(request):
    meta = Mentor._meta

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{meta.verbose_name_plural}.csv"'},
    )

    fields, names = zip(*[(field.name, field.verbose_name) for field in meta.get_fields()[1:]])

    writer = csv.writer(response)
    writer.writerow(names)

    for obj in Mentor.objects.all():
        writer.writerow([getattr(obj, field) for field in fields])

    return response


class MentorCreateView(CreateView):
    model = Mentor
    form_class = MentorForm
    success_url = reverse_lazy('mentoring:mentor-create-done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        moment = timezone.now()
        context['registration_is_open'] = Registration.objects.filter(started_at__lte=moment,
                                                                      stopped_at__gte=moment).exists()
        return context

    def form_valid(self, form):
        moment = timezone.now()
        try:
            registration = Registration.objects.get(started_at__lte=moment, stopped_at__gte=moment)
        except Registration.DoesNotExist:
            messages.error(self.request, _("Registration is closed."))
            raise PermissionDenied()
        form.instance.registration = registration
        return super().form_valid(form)


class MentorCreateDoneView(TemplateView):
    template_name = 'mentoring/mentor_form_done.html'


class MentorDetailView(LoginRequiredMixin, DetailView):
    model = Mentor
