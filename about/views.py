from django.views import generic

from .models import Image


class AboutView(generic.TemplateView):
    template_name = 'about/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = Image.objects.first()
        return context
