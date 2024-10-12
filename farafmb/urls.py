from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("consultations/", include("consultations.urls")),
    path("documents/", include("documents.urls")),
    path("exams/", include("exams.urls")),
    path("jobs/", include("jobs.urls")),
    path("links/", include("links.urls")),
    path("meetings/", include("meetings.urls")),
    path("members/", include("members.urls")),
    path("excursions/", include("excursions.urls")),
    path("i18n/", include("django.conf.urls.i18n")),  # required
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
