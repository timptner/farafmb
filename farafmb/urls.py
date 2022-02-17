from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path, reverse
from oauth2_provider.views import ConnectDiscoveryInfoView


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
    path('consultations/', include('consultations.urls')),
    path('excursions/', include('excursions.urls')),
    path('jobs/', include('jobs.urls')),
    path('meetings/', include('meetings.urls')),
    path('members/', include('members.urls')),
    re_path(r'^oauth/\.well-known/openid-configuration/?$',
            ConnectDiscoveryInfoView.as_view(),
            name='oidc-connect-discovery-info'),  # Serve discovery view on both routes
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
