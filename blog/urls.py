from django.shortcuts import redirect
from django.urls import path, reverse

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('links/', views.LinksView.as_view(), name='links'),
    path('protocols/', lambda request: redirect(reverse('exams:submit'), permanent=True)),
]
