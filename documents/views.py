from django.views.generic import ListView

from .models import Document


class DocumentListView(ListView):
    template_name = 'documents/document_list.html'
    queryset = Document.objects.filter(visible=True).order_by('group', 'title')
