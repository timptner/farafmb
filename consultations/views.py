from datetime import time
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


class ConsultationListView(LoginRequiredMixin, generic.ListView):
    model = Consultation
    queryset = Consultation.objects.all()
    ordering = ['day', 'start']


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


class OfficeHoursView(generic.TemplateView):
    template_name = 'consultations/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        earliest = min(Consultation.objects.values_list('start', flat=True))
        latest = max(Consultation.objects.values_list('end', flat=True))
        context['earliest'] = earliest
        context['latest'] = latest
        data = {
            'hours': [time(hour=hour) for hour in range(earliest.hour, latest.hour + 1)],
        }
        for day, display in Consultation.DAYS:
            data[day] = []
            for hour in range(earliest.hour, latest.hour + 1):
                data[day].append(
                    Consultation.objects.filter(day=day, start__hour=hour).all()
                )
        context['data'] = map(list, zip(*data.values()))  # transpose matrix
        context['days'] = Consultation.DAYS
        return context
