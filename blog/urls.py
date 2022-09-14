from django.shortcuts import redirect
from django.urls import path, reverse

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.LatestPostsView.as_view(), name='news'),
    path('archive/', views.PostsView.as_view(), name='archive'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/add/', views.PostCreateView.as_view(), name='create-post'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('protocols/', lambda request: redirect(reverse('exams:submit'), permanent=True)),
]
