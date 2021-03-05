from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('meetings/', include('meetings.urls')),
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
]
