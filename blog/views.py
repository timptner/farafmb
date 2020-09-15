from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Snippet, Post, Image


class IndexView(generic.TemplateView):
    template_name = 'blog/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = get_object_or_404(Snippet, slug='landing_page')
        try:
            context['image'] = Image.objects.get(slug='landing_page')

        except ObjectDoesNotExist:
            pass

        return context


class BlogView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'blog/pages/blog.html'
    ordering = ['-created']


class OfficeHoursView(generic.TemplateView):
    template_name = 'blog/pages/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = get_object_or_404(Snippet, slug='office_hours')
        return context
