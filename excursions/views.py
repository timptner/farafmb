from django.shortcuts import render
from django.views import generic

from .models import Excursion


class ExcursionListView(generic.ListView):
    model = Excursion
