from django.template.defaultfilters import date
from django.views import generic

from .models import Snippet, Post, Image


class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = 'homepage'
        context['snippet'] = Snippet.objects.filter(slug='homepage').first()
        context['image'] = Image.objects.filter(slug='homepage').first()
        return context


class PostsView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/posts.html'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archive'] = []
        year_list = Post.objects.dates('created', 'year')
        for dt in year_list:
            month_list = Post.objects.filter(created__year=dt.year).dates('created', 'month')
            context['archive'].append((dt, month_list))
        return context


class OfficeHoursView(generic.TemplateView):
    template_name = 'blog/office_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippet'] = Snippet.objects.filter(slug='office_hours').first()
        return context


class PostArchiveIndexView(generic.dates.ArchiveIndexView):
    model = Post
    date_field = 'created'


class PostYearArchiveView(generic.dates.YearArchiveView):
    model = Post
    date_field = 'created'
    make_object_list = True


class PostMonthArchiveView(generic.dates.MonthArchiveView):
    model = Post
    date_field = 'created'


class PostDayArchiveView(generic.dates.DayArchiveView):
    model = Post
    date_field = 'created'
