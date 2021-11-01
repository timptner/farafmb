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
        context['text'] = """
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

