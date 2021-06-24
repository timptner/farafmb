from django.shortcuts import render
from django.views import generic

from .models import OfficeHour
from .utils import calc_max_step_size, time_to_seconds, seconds_to_time


class OfficeHoursView(generic.TemplateView):
    template_name = 'office_hours/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        office_hours = OfficeHour.objects.filter(is_visible=True).all()
        time_list = [office_hour.time for office_hour in office_hours]
        seconds = calc_max_step_size(time_list)
        points = range(
            time_to_seconds(min(time_list)),
            time_to_seconds(max(time_list)) + seconds + seconds,
            seconds,
        )

        context['data'] = {}
        for time_ in [seconds_to_time(seconds) for seconds in points]:
            slots = []
            for day, name in OfficeHour.DAYS:
                if time_ in time_list:
                    slots.append(office_hours.filter(time=time_, day=day).all())
                else:
                    slots.append([])
            context['data'][time_] = slots
        context['days'] = OfficeHour.DAYS
        return context
