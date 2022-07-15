from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import MentorForm
from .models import Mentor


class MentorCreateView(LoginRequiredMixin, CreateView):
    model = Mentor
    form_class = MentorForm
    success_url = reverse_lazy('create-mentor-done')


class MentorCreateDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'mentoring/mentor_form_done.html'


class MentorListView(LoginRequiredMixin, ListView):
    template_name = 'mentoring/mentor_list.html'
    model = Mentor
