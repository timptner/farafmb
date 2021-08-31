from django.views import generic
from django.contrib.auth.models import User

from .models import Profile


class MemberListView(generic.ListView):
    model = User
    template_name = 'members/member_list.html'

    def get_queryset(self):
        user_list = Profile.objects.values_list('user', flat=True).all()
        return User.objects.filter(pk__in=user_list).all()
