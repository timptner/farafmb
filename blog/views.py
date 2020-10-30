from django.views import generic

from .models import Snippet, Post, Image


class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'homepage'
        context['snippet'] = Snippet.objects.filter(slug='homepage').first()
        context['image'] = Image.objects.filter(slug='homepage').first()
        return context


class PostsView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/posts.html'
    ordering = ['-created']


class OfficeHoursView(generic.TemplateView):
    template_name = 'blog/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = Snippet.objects.filter(slug='office_hours').first()
        return context
