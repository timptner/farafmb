from django.urls import path

from . import views

app_name = 'docs'
urlpatterns = [
    path('', views.show_tree, {'page': '/'}, name='index'),
    path('edit/<path:page>', views.update_page, name='update_page'),
    path('delete/<path:page>', views.delete_page, name='delete_page'),
    path('new/', views.create_page, name='create_page'),
    path('read/<path:page>', views.read_page, name='read_page'),
    path('tree/', views.show_tree, {'page': '/'}, name='index_show_tree'),
    path('tree/<path:page>/', views.show_tree, name='show_tree'),
]
