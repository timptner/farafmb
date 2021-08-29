from django.views import generic
from django.contrib.auth.models import User


class MemberList(generic.ListView):
    model = User
    template_name = 'members/list.html'
