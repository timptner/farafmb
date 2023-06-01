from django.urls import path

from . import views

app_name = 'excursions'
urlpatterns = [
    path('contact/', views.ContactFormView.as_view(), name='contact'),
]
