from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('blog.urls')),
    path('about/', include('about.urls')),
    path('consultations/', include('consultations.urls')),
    path('documents/', include('documents.urls')),
    path('events/', include('events.urls')),
    path('exams/', include('exams.urls')),
    path('excursions/', include('excursions.urls')),
    path('jobs/', include('jobs.urls')),
    path('links/', include('links.urls')),
    path('meetings/', include('meetings.urls')),
    path('members/', include('members.urls')),
    path('mentoring/', include('mentoring.urls')),
    path('merchandise/', include('merchandise.urls')),

    prefix_default_language=True
)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
