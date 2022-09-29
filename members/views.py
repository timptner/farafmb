import secrets

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import UserProfileForm, UserForm
from .models import Profile


class MemberListView(generic.ListView):
    model = User
    template_name = 'members/member_list.html'

    def get_queryset(self):
        user_list = Profile.objects.values_list('user', flat=True).all()
        return User.objects.filter(pk__in=user_list).order_by('profile__joined_at')


class UserProfileFormView(LoginRequiredMixin, generic.FormView):
    template_name = 'members/profile_form.html'
    success_url = reverse_lazy('members:profile_form')
    form_class = UserProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        if hasattr(user, 'profile'):
            initial.update({
                'picture': user.profile.picture,
                'biography': user.profile.biography,
                'jobs': user.profile.jobs,
                'course': user.profile.course,
                'degree': user.profile.degree,
                'birthday': user.profile.birthday,
                'joined_at': user.profile.joined_at,
            })
        return initial

    def form_valid(self, form):
        user = self.request.user

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        if hasattr(user, 'profile'):
            profile = user.profile
        else:
            profile = Profile(user=user)
        profile.picture = form.cleaned_data['picture']
        profile.biography = form.cleaned_data['biography']
        profile.jobs = form.cleaned_data['jobs']
        profile.course = form.cleaned_data['course']
        profile.degree = form.cleaned_data['degree']
        profile.birthday = form.cleaned_data['birthday']
        profile.joined_at = form.cleaned_data['joined_at']
        profile.save()

        messages.success(self.request, "Dein Profil wurde erfolgreich aktualisiert.")

        return super().form_valid(form)


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'auth.add_user'
    template_name = 'members/create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('members:create_user')

    def form_valid(self, form):
        default_group, created = Group.objects.get_or_create(name='default')
        password = secrets.token_urlsafe(16)

        user = form.save(commit=False)
        user.password = make_password(password)
        user.is_staff = True
        user.save()
        user.groups.add(default_group)

        form.send_email(self.request, user, password)

        messages.success(self.request, "Es wurde eine E-Mail mit Zugangsdaten an '%s' geschickt." % user.email)

        return super().form_valid(form)


def get_profile(request):
    return redirect(reverse('members:member-update', args=[request.user.pk]))
