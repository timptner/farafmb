from django.urls import path

from . import views

app_name = 'office-hours'
urlpatterns = [
    path('', views.OfficeHoursView.as_view(), name='main'),
]