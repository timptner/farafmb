from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from .forms import ProtocolForm
from .models import Snippet, Post, Image, Document


class AboutView(TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['snippet'] = get_object_or_404(Snippet, slug='about')

        try:
            context['image'] = Image.objects.get(slug='about')
        except ObjectDoesNotExist:
            pass

        return context


class OfficeHoursView(TemplateView):
    template_name = 'blog/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = get_object_or_404(Snippet, slug='office_hours')

        try:
            context['table'] = Snippet.objects.get(slug='office_hours_table')
        except ObjectDoesNotExist:
            pass

        return context


class PostsView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']


class DocumentsView(ListView):
    template_name = 'blog/documents.html'
    model = Document


class ContactView(TemplateView):
    template_name = 'blog/contact.html'


class ProtocolView(FormView):
    template_name = 'blog/protocol_form.html'
    form_class = ProtocolForm
    success_url = reverse_lazy('blog:protocols-success')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ProtocolSuccessView(TemplateView):
    template_name = 'blog/protocol_form_done.html'
