from datetime import date
from django.views.generic import TemplateView, ListView
from meetings.models import Meeting

from .models import Post


class PostsView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']
    paginate_by = 10


class LatestPostsView(ListView):
    template_name = 'blog/latest_posts.html'
    queryset = Post.objects.order_by('-created').all()[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['meetings'] = Meeting.objects.filter(date__gte=date.today())
        return context


class ContactView(TemplateView):
    template_name = 'blog/contact.html'
