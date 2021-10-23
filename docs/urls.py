from django.urls import path

from . import views

app_name = 'docs'
urlpatterns = [
    path('', views.list_pages, name='list_pages'),
    path('<path:resource>/_delete', views.delete_page, name='delete_page'),
    path('<path:resource>/_edit', views.update_page, name='update_page'),
    path('<path:resource>', views.read_page, name='read_page'),
]
