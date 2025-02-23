from django.test import TestCase

from .models import Member


class MemberListTest(TestCase):
    def setUp(self) -> None:
        self.member = Member.objects.create(
            name="Nala",
            email="nala@example.org",
            picture="/dev/null",
            statement="Aus einer einjährigen Patenschaft entstand langjährige Verbundenheit",
            department=Member.MENTORING,
            program="MB-B",
            birthday="2011-12-24",
            joined_at="2012-08-01",
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
