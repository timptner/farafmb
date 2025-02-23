from django.views import generic

from .models import Member


class MemberListView(generic.ListView):
    model = Member
    template_name = 'members/member_list.html'
    ordering = ["name"]

    def get_queryset(self, **kwargs) -> list:
        departments = {pk: [] for pk, label in Member.DEPARTMENT_CHOICES}
        for member in super().get_queryset(**kwargs):
            departments[member.department].append(member)

        return [(label, departments[pk]) for pk, label in Member.DEPARTMENT_CHOICES]
