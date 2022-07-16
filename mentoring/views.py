import csv

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import RegistrationForm, ProgramForm, MentorForm, HelperForm
from .models import Registration, Program, Mentor, Helper


def export_as_csv(model):
    meta = model._meta

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{meta.verbose_name_plural}.csv"'},
    )

    fields, names = zip(*[(field.name, field.verbose_name) for field in meta.get_fields()[1:]])

    writer = csv.writer(response)
    writer.writerow(names)

    for obj in model.objects.all():
        writer.writerow([getattr(obj, field) for field in fields])

    return response


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


def export_mentors_as_csv(request):
    return export_as_csv(Mentor)


class MentorCreateView(LoginRequiredMixin, CreateView):
    model = Mentor
    form_class = MentorForm
    success_url = reverse_lazy('mentoring:mentor-create-done')


class MentorCreateDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'mentoring/mentor_form_done.html'


class MentorDetailView(LoginRequiredMixin, DetailView):
    model = Mentor


class HelperListView(LoginRequiredMixin, ListView):
    model = Helper


def export_helpers_as_csv(request):
    return export_as_csv(Helper)


class HelperCreateView(LoginRequiredMixin, CreateView):
    model = Helper
    form_class = HelperForm
    success_url = reverse_lazy('mentoring:helper-create-done')


class HelperCreateDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'mentoring/helper_form_done.html'


class HelperDetailView(LoginRequiredMixin, DetailView):
    model = Helper
