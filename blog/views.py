from datetime import date
from django.views.generic import TemplateView, ListView
from meetings.models import Meeting

from .models import Post, Link


class PostsView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['meetings'] = Meeting.objects.filter(date__gte=date.today())
        return context


class ContactView(TemplateView):
    template_name = 'blog/contact.html'


class LinksView(ListView):
    template_name = 'blog/links.html'
    model = Link
    queryset = Link.objects.filter(visible=True)
