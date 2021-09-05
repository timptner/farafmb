from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('meetings/', include('meetings.urls')),
    # path('members/', include('members.urls')),
    path('office-hours/', include('office_hours.urls')),
]
