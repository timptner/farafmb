from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import ConsultationForm
from .models import Consultation
from .utils import calc_max_step_size, time_to_seconds, seconds_to_time


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


class ConsultationsView(generic.TemplateView):
    template_name = 'consultations/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = {}
        office_hours = Consultation.objects.filter(is_visible=True).all()
        if office_hours:
            time_list = [office_hour.time for office_hour in office_hours]
            seconds = calc_max_step_size(time_list)
            if seconds == 0:
                seconds = 7200
            points = range(
                time_to_seconds(min(time_list)),
                time_to_seconds(max(time_list)) + seconds + seconds,
                seconds,
            )
            for time_ in [seconds_to_time(seconds) for seconds in points]:
                slots = []
                for day, name in Consultation.DAYS:
                    if time_ in time_list:
                        slots.append(office_hours.filter(time=time_, day=day).all())
                    else:
                        slots.append([])
                context['data'][time_] = slots
        context['days'] = Consultation.DAYS
        return context
