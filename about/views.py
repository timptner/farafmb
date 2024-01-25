from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .forms import ImageForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Das Gruppenbild wurde aktualisiert!")
            return HttpResponseRedirect(reverse('about:index'))
    else:
        form = ImageForm()
    return render(request, 'about/upload.html', {'form': form})


class AboutView(generic.TemplateView):
    template_name = 'about/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = default_storage.url('about/team.jpeg') if default_storage.exists('about/team.jpeg') else None
        return context
