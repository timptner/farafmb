import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django_s3_storage.storage import S3Storage

from .forms import PageForm

storage = S3Storage(
    aws_region=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_s3_bucket_name=os.getenv('DO_SPACE_NAME_DOCS', 'farafmb-docs'),
    aws_s3_endpoint_url=os.getenv('DO_SPACE_ENDPOINT_URL_DOCS', 'https://fra1.digitaloceanspaces.com'),
    aws_s3_file_overwrite=True,
)


def get_breadcrumbs(request, page):
    breadcrumbs = []
    if page != '/':
        names = page.split('/')
        for name in names:
            page_ = '/'.join([names[i] for i in range(names.index(name) + 1)])
            breadcrumbs.append((name, request.build_absolute_uri(reverse('docs:show_tree', args=(page_,)))))
    breadcrumbs.insert(0, ('Dokumentation', request.build_absolute_uri(reverse('docs:index_show_tree'))))
    return breadcrumbs


@login_required
def show_tree(request, page):
    prefix = '' if page == '/' else page + '/'
    directories, files = storage.listdir(page)
    context = {
        'page': page,
        'directories': [(name, prefix + name) for name in directories],
        'files': [(name, prefix + name) for name in files],
        'breadcrumbs': get_breadcrumbs(request, page),
    }
    return render(request, 'docs/show_tree.html', context)


@login_required
def create_page(request):
    page = request.GET.get('page')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page_ = form.cleaned_data['title'] + '.md'
            file = ContentFile(content=form.cleaned_data['content'], name=page_)
            storage.save(name=file.name, content=file)
            return HttpResponseRedirect(reverse('docs:read_page', args=(page_,)))
    else:
        initial_title = "Neue Seite" if page == '/' else page.replace('_', ' ') + "/Neue Seite"
        form = PageForm(initial={'title': initial_title})
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'docs/create_page.html', context=context)


@login_required
def read_page(request, page):
    navigation = []
    dirs, files = storage.listdir(page)
    for name in dirs:
        navigation.append({
            'name': name,
            'icon': 'directory',
            'url': f"{page}/{name}" if page != '/' else name,
        })
    for name in files:
        navigation.append({
            'name': name,
            'icon': 'file',
            'url': f"{page}/{name.rstrip('.md')}" if page != '/' else name.rstrip('.md'),
        })
    context = {
        'page': page,
        'navigation': navigation,
        'breadcrumbs': get_breadcrumbs(request, page),
        'content': storage.open(page).read().decode('utf-8'),
    }
    return render(request, 'docs/read_page.html', context=context)


@login_required
def update_page(request, page):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            file = ContentFile(form.cleaned_data['content'], name=page)
            storage.save(name=file.name, content=file)
            return HttpResponseRedirect(reverse('docs:read_page', args=(page,)))
    else:
        content = storage.open(page).read().decode('utf-8')
        form = PageForm(initial={'title': page.replace('_', ' ').rstrip('.md'), 'content': content})
        form.fields['title'].help_text = "Die Umbenennung von Seiten wird zurzeit noch nicht unterstützt."
    context = {
        'page': page,
        'title': page.replace('_', ' ').split('/')[-1],
        'form': form,
    }
    return render(request, 'docs/update_page.html', context=context)


@login_required
def delete_page(request, page):
    if request.method == 'POST':
        storage.delete(page)
        messages.add_message(request, messages.SUCCESS, f'Die Seite "{page}" wurde erfolgreich gelöscht.')
        return HttpResponseRedirect(reverse('docs:index_show_tree'))
    else:
        return HttpResponse(status=204)
