from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from meetings.models import Meeting

from .forms import PostCreateForm
from .models import Post


class PostListView(LoginRequiredMixin, generic.ListView):
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


class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']
    paginate_by = 10


class LatestPostsView(generic.ListView):
    template_name = 'blog/news.html'
    queryset = Post.objects.order_by('-created').all()[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['meetings'] = Meeting.objects.filter(date__gte=date.today())
        return context


class ContactView(generic.TemplateView):
    template_name = 'blog/contact.html'
