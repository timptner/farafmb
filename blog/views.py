from consultations.models import Consultation
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic
from meetings.models import Meeting

from .forms import PostCreateForm
from .models import Post, Event


class PostListView(generic.ListView):
    model = Post
    paginate_by = 6


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    form_class = PostCreateForm
    success_message = _("%(title)s was created successfully")

    def get_success_url(self):
        return reverse('blog:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArchiveView(generic.ListView):
    template_name = 'blog/archive.html'
    model = Post
    ordering = ['-created']
    paginate_by = 10


class ContactView(generic.TemplateView):
    template_name = 'blog/contact.html'


class MerchandiseView(generic.TemplateView):
    template_name = 'blog/merchandise.html'


class ExcursionView(generic.TemplateView):
    template_name = 'blog/excursions.html'
