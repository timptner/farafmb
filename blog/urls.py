from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('sprechzeiten/', views.OfficeHoursView.as_view(), name='office_hours'),

    path('archiv/',
         views.PostArchiveIndexView.as_view(), name='post_archive'),
    path('archiv/<int:year>/',
         views.PostYearArchiveView.as_view(), name='post_year_archive'),
    path('archiv/<int:year>/<int:month>/',
         views.PostMonthArchiveView.as_view(month_format='%m'), name='post_month_archive'),
    path('archiv/<int:year>/<int:month>/<int:day>/',
         views.PostDayArchiveView.as_view(month_format='%m'), name='post_day_archive'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
