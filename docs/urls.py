from django.urls import path

from . import views

app_name = 'docs'
urlpatterns = [
    path('', views.list_pages, name='list_pages'),
    path('<path:resource>', views.read_page, name='read_page'),
]
