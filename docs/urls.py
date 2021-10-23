from django.urls import path

from . import views

app_name = 'docs'
urlpatterns = [
    path('', views.list_pages, name='list_pages'),
    path('_new', views.create_page, {'page': '/'}, name='create_page_index'),
    path('<path:page>/_edit', views.update_page, name='update_page'),
    path('<path:page>/_delete', views.delete_page, name='delete_page'),
    path('<path:page>/_new', views.create_page, name='create_page'),
    path('<path:page>', views.read_page, name='read_page'),
]
