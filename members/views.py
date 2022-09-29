from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import UserForm, MemberForm
from .models import Member


class MemberListView(generic.ListView):
    model = Member
    template_name = 'members/member_list.html'
    ordering = ['joined_at']


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    permission_required = 'auth.add_user'
    template_name = 'members/user_form.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('members:user-create')
    success_message = _("New user \"%(first_name)s %(last_name)s\" was created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):
        default_group, created = Group.objects.get_or_create(name='default')

        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        user.groups.add(default_group)

        form.send_email(user, self.request)

        return super().form_valid(form)


class MemberCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    model = Member
    form_class = MemberForm
    success_message = _("You successfully created your profile")

    def test_func(self):
        return not Member.objects.filter(user=self.request.user).exists()

    def form_valid(self, form):
        member = form.save(commit=False)
        member.user = self.request.user
        member.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('members:member-update', kwargs={'pk': self.object.pk})


class MemberUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Member
    form_class = MemberForm
    success_message = _("You successfully updated your profile")

    def test_func(self):
        return self.request.user.member

    def get_success_url(self):
        return reverse_lazy('members:member-update', kwargs={'pk': self.object.pk})
