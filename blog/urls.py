from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('documents/', views.DocumentsView.as_view(), name='documents'),
    path('links/', views.LinksView.as_view(), name='links'),
    path('protocols/', views.ProtocolView.as_view(), name='protocols'),
    path('protocols/success/', views.ProtocolSuccessView.as_view(), name='protocols-success'),
]
