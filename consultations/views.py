from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import ConsultationForm
from .models import Consultation


class ConsultationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Consultation
    form_class = ConsultationForm
    success_url = reverse_lazy('consultations:consultation-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context


class ConsultationListView(generic.ListView):
    model = Consultation
    queryset = Consultation.objects.all()


class ConsultationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Consultation
    form_class = ConsultationForm
    success_url = reverse_lazy('consultations:consultation-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class ConsultationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Consultation
    success_url = reverse_lazy('consultations:consultation-list')
