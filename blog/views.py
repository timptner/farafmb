from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Snippet


class IndexView(generic.TemplateView):
    template_name = 'blog/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = get_object_or_404(Snippet, key='index')
        return context
