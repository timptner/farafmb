from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('documents/', views.DocumentsView.as_view(), name='documents'),
    path('office-hours/', views.OfficeHoursView.as_view(), name='office-hours'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
