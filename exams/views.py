from django.views import generic
from django.urls import reverse_lazy

from .forms import SubmitForm


class InfoView(generic.TemplateView):
    template_name = 'exams/info.html'


class SubmitView(generic.CreateView):
    template_name = 'exams/submit_form.html'
    form_class = SubmitForm
    success_url = reverse_lazy('exams:submit_done')


class SubmitDoneView(generic.TemplateView):
    template_name = 'exams/submit_done.html'
