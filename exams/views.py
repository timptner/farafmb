from django.views import generic
from django.urls import reverse_lazy

from .forms import ExamSubmitForm


class InfoView(generic.TemplateView):
    template_name = 'exams/info.html'


class ExamSubmitView(generic.CreateView):
    template_name = 'exams/exam_submit_form.html'
    form_class = ExamSubmitForm
    success_url = reverse_lazy('exams:submit_done')


class ExamSubmitDoneView(generic.TemplateView):
    template_name = 'exams/exam_submit_done.html'
