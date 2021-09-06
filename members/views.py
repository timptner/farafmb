from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserProfileForm
from .models import Profile


class MemberListView(generic.ListView):
    model = User
    template_name = 'members/member_list.html'

    def get_queryset(self):
        user_list = Profile.objects.values_list('user', flat=True).all()
        return User.objects.filter(pk__in=user_list).all()


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
            'picture': user.profile.picture,
            'biography': user.profile.biography,
            'jobs': user.profile.jobs,
            'course': user.profile.course,
            'birthday': user.profile.birthday,
        })
            'joined_at': user.profile.joined_at,
        return initial

    def form_valid(self, form):
        user = self.request.user

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        profile = user.profile
        profile.picture = form.cleaned_data['picture']
        profile.biography = form.cleaned_data['biography']
        profile.jobs = form.cleaned_data['jobs']
        profile.course = form.cleaned_data['course']
        profile.birthday = form.cleaned_data['birthday']
        profile.joined_at = form.cleaned_data['joined_at']
        profile.save()

        messages.success(self.request, "Dein Profil wurde erfolgreich aktualisiert.")

        return super().form_valid(form)
