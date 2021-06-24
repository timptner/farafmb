from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('meetings/', include('meetings.urls')),
    path('office-hours/', include('office_hours.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
