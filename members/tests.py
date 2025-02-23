from django.test import TestCase

from .models import Member


class MemberListTest(TestCase):
    def setUp(self) -> None:
        self.member = Member.objects.create(
            name="Nala",
            email="nala@example.org",
            picture="members/nala.png",
            statement="Aus einer einjährigen Patenschaft entstand langjährige Verbundenheit",
            department=Member.MENTORING,
            program="MB-B",
            birthday="2011-12-24",
            joined_at="2012-08-01",
            is_visible=True,
            is_alumnus=True,
        )
        self.member_hidden = Member.objects.create(
            name="John",
            email="john@example.org",
            picture="members/john.png",
            statement="",
            department=Member.ADMINISTRATION,
            program="IDE",
            birthday="2000-01-01",
            joined_at="2025-02-03",
            is_visible=False,
            is_alumnus=False,
        )

    def test_member_list_view(self) -> None:
        response = self.client.get("/mitglieder/")
        self.assertContains(response, self.member.name)
        self.assertNotContains(response, self.member.email)
        self.assertContains(response, f'<img src="{self.member.picture.url}" alt="Bild von {self.member.name }">', html=True)
        self.assertContains(response, self.member.statement)
        self.assertContains(response, self.member.get_department_display())
        self.assertContains(response, self.member.get_program_display())
        self.assertNotContains(response, self.member.birthday)
        self.assertContains(response, "Studium abgeschlossen")

        self.assertNotContains(response, self.member_hidden.name)
        self.assertNotContains(response, self.member_hidden.email)
        self.assertNotContains(response, self.member_hidden.picture.url)
