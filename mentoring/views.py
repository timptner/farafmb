from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import ProgramForm, MentorForm
from .models import Program, Mentor


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


class MentorCreateView(LoginRequiredMixin, CreateView):
    model = Mentor
    form_class = MentorForm
    success_url = reverse_lazy('mentoring:mentor-create')


class MentorCreateDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'mentoring/mentor_form_done.html'
