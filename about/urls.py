from django.urls import path

from . import views

app_name = 'about'
urlpatterns = [
    path('', views.AboutView.as_view(), name='index'),
    path('upload/', views.upload_file, name='upload-form'),
]
