from django.views.generic import DetailView
from django.utils import timezone

from .models import Team


class LandingPageView(DetailView):
    model = Team
    template_name = "home/landing_page.html"

    def get_object(self, queryset=None):
        return (
            Team.objects.exclude(release_date__gt=timezone.now().date())
            .order_by("-release_date")
            .first()
        )
