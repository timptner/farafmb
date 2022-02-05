from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('about/', include('about.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # TODO Remove default auth views
    path('admin/', admin.site.urls),
    path('excursions/', include('excursions.urls')),
    path('jobs/', include('jobs.urls')),
    path('meetings/', include('meetings.urls')),
    path('members/', include('members.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('office-hours/', include('office_hours.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
