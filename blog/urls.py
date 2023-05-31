from django.shortcuts import redirect
from django.urls import path, reverse

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.NewsView.as_view(), name='news'),
    path('archive/', views.ArchiveView.as_view(), name='archive'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/add/', views.PostCreateView.as_view(), name='create-post'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('protocols/', lambda request: redirect(reverse('exams:submit'), permanent=True)),
    path('merchandise/', views.MerchandiseView.as_view(), name='merchandise'),
    path('excursions/', views.ExcursionView.as_view(), name='excursions'),
]
