from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('excursions/', include('excursions.urls')),
    path('jobs/', include('jobs.urls')),
    path('meetings/', include('meetings.urls')),
    path('members/', include('members.urls')),
    path('office-hours/', include('office_hours.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
