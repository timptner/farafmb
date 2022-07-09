from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.MentorCreateView.as_view(), name='create-mentor'),
]
