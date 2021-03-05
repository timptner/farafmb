from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from meetings.forms import InviteForm
from meetings.models import Meeting


class SendInvite(LoginRequiredMixin, FormView):
    template_name = 'meetings/invite_form.html'
    form_class = InviteForm
    success_url = 'success/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['meeting'] = get_object_or_404(Meeting, date=self.request.GET.get('date'))
        return kwargs

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class SendInviteSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'meetings/invite_form_success.html'
