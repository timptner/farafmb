from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .forms import ImageForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Das Gruppenbild wurde aktualisiert!")
            return HttpResponseRedirect(reverse('blog:about'))  # TODO change to new url
    else:
        form = ImageForm()
    return render(request, 'about/upload.html', {'form': form})

