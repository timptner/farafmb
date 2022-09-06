from django.shortcuts import redirect
from django.urls import path, reverse

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.LatestPostsView.as_view(), name='latest_posts'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('protocols/', lambda request: redirect(reverse('exams:submit'), permanent=True)),
]
