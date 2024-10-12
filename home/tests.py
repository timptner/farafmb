from datetime import timedelta

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Team
from .views import LandingPageView


class TeamTest(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(label="Gruppenbild", release_date="2024-10-12")

    def test_team_is_named_by_label(self) -> None:
        """Team is namd by attribut 'label'"""
        self.assertEqual(str(self.team), self.team.label)


class LandingPageTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.today = timezone.now().date()
        Team.objects.bulk_create(
            [
                Team(
                    label="Gruppenbild",
                    release_date=self.today + timedelta(days=days),
                )
                for days in [-7, -3, 1, 5]
            ]
        )

    def test_expected_team_in_view(self) -> None:
        """Currently released team is shown"""
        team = Team.objects.get(release_date=self.today + timedelta(days=-3))

        request = self.factory.get(reverse("home:landing_page"))
        view = LandingPageView()
        view.setup(request)

        object = view.get_object()
        self.assertEqual(object, team)
