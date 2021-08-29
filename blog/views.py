import random

from blog.forms import ProtocolForm
from blog.models import Snippet, Post, Image, Document, Protocol, Link
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from meetings.models import Meeting


class AboutView(TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_about'] = """
Wenn wir uns gerade mal nicht mit den Professorinnen und Professoren um bessere Noten für uns selbst streiten, kämpfen 
wir als Fachschaftsrat mit Händen und Füßen jeden Tag dafür die 
[Otto-von-Guericke-Universität Magdeburg](https://www.ovgu.de) und unsere 
[Fakultät für Maschinenbau](https://www.fmb.ovgu.de) ein kleines Stück besser zu machen.

Wir sind das offizielle Vertretungsgremium der Studierenden an der Fakultät für Maschinenbau. Das heißt wir setzen uns 
dafür ein, dass eure Vorschläge und auch eure Kritik an die Fakultät herangetragen wird. Die weiteren Aufgaben, die wir 
bewältigen, sind in unserer Satzung für euch alle online nachzulesen.

Wie versuchen uns kontinuierlich zu verbessern und euch Informationen über Neuerungen an der Universität leichter 
zugänglich zu machen. Außerdem setzen wir uns dafür ein euch eine einfachere Kommunikation mit den Professoren zu 
ermöglichen und euch bessere und wechselnde Veranstaltungen zu bieten.

Um dies kontinuierlich durchsetzen zu können brauchen wir auch immer neuen Input und freuen uns somit über neue 
Mitglieder, die neue Ansichten und Dynamiken bei uns in den Fachschaftsrat bringen.

\#jointhecrew

---

_English_

When we are not fighting with the professors for better grades for ourselves, we as the student council fight tooth and 
nail every day to make [Otto von Guericke University Magdeburg](https://www.ovgu.de/en/) and our 
[Faculty of Mechanical Engineering](https://www.fmb.ovgu.de/en/) a little bit better.

We are the official representative body of the students at the Faculty of Mechanical Engineering. This means that we 
make sure that your suggestions and also your criticism are brought to the attention of the faculty. The other tasks we 
deal with can be read online in our constitution.

We try to improve ourselves continuously and to make information about innovations at the university more accessible to 
you. We are also committed to making it easier for you to communicate with your professors and to offer you better and 
more varied events.

In order to be able to implement this continuously, we always need new input and are therefore happy to welcome new 
members who bring new views and dynamics to the student council.

\#jointhecrew
"""
        return context


class PostsView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['meetings'] = Meeting.objects.filter(date__gte=date.today())
        return context


class DocumentsView(ListView):
    template_name = 'blog/documents.html'
    model = Document
    queryset = Document.objects.filter(visible=True)


class ContactView(TemplateView):
    template_name = 'blog/contact.html'


class ProtocolView(CreateView):
    model = Protocol
    template_name = 'blog/protocol_form.html'
    form_class = ProtocolForm
    success_url = reverse_lazy('blog:protocols-success')

    def form_valid(self, form):
        form.instance.file.name = hex(random.randrange(16 ** 8))[2:] + '.pdf'
        return super().form_valid(form)


class ProtocolSuccessView(TemplateView):
    template_name = 'blog/protocol_form_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['snippet'] = get_object_or_404(Snippet, slug='protocol_submitted')
        return context


class LinksView(ListView):
    template_name = 'blog/links.html'
    model = Link
    queryset = Link.objects.filter(visible=True)
