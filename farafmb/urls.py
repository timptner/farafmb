from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse


def redirect_admin(request):
    base_url = reverse('login')
    if 'next' in request.GET:
        url = f"{base_url}?next={request.GET.get('next')}"
    else:
        url = base_url
    return redirect(url)


urlpatterns = [
    path('', include('blog.urls')),
    path('about/', include('about.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/login/', redirect_admin),
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
