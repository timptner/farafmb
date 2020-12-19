from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Snippet, Post, Image


class AboutView(generic.TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['snippet'] = get_object_or_404(Snippet, slug='about')

        try:
            context['image'] = Image.objects.get(slug='about')
        except ObjectDoesNotExist:
            pass

        return context


class OfficeHoursView(generic.TemplateView):
    template_name = 'blog/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = get_object_or_404(Snippet, slug='office_hours')

        try:
            context['table'] = Snippet.objects.get(slug='office_hours_table')
        except ObjectDoesNotExist:
            pass

        return context


class PostsView(generic.ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']
