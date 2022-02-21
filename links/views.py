from django.views import generic

from .models import Link


class IndexView(generic.ListView):
    template_name = 'links/index.html'
    model = Link
    queryset = Link.objects.filter(is_active=True)
