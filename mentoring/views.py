from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import MentorForm
from .models import Mentor


class MentorCreateView(LoginRequiredMixin, CreateView):
    model = Mentor
    form_class = MentorForm
