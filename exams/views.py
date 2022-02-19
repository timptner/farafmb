from django.views import generic


class InfoView(generic.TemplateView):
    template_name = 'exams/info.html'
