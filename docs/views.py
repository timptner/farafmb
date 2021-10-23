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


@login_required
def show_tree(request, page):
    prefix = '' if page == '/' else page + '/'
    directories, files = storage.listdir(page)
    context = {
        'directories': [(name, prefix + name) for name in directories],
        'files': [(name, prefix + name) for name in files],
    }
    return render(request, 'docs/show_tree.html', context)


@login_required
def list_pages(request):
    response = storage.s3_connection.list_objects_v2(Bucket=storage.settings.AWS_S3_BUCKET_NAME)
    pages = []
    for entry in response.get('Contents', []):
        key = entry['Key'].rstrip('.md')
        pages.append({'key': key, 'name': key.replace('_', ' ')})
    return render(request, 'docs/list_pages.html', {'pages': pages})


@login_required
def create_page(request, page):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            file = ContentFile(content=form.cleaned_data['content'], name=form.cleaned_data['title'] + '.md')
            storage.save(name=file.name, content=file)
            return HttpResponseRedirect(reverse('docs:read_page', args=(form.cleaned_data['title'],)))
    else:
        initial_title = "Neue Seite" if page == '/' else page.replace('_', ' ') + "/Neue Seite"
        form = PageForm(initial={'title': initial_title})
    context = {
        'page': page,
        'title': page.replace('_', ' ').split('/')[-1],
        'form': form,
    }
    return render(request, 'docs/create_page.html', context=context)


@login_required
def read_page(request, page):
    content = storage.open(page + '.md').read().decode('utf-8')
    breadcrumbs = []
    for name in page.split('/'):
        breadcrumbs.append({
            'name': name.replace('_', ' '),
            'url': '/'.join([breadcrumbs[-1]['url'], name]) if breadcrumbs else name,
            'is_active': False,
        })
    breadcrumbs.insert(0, {
        'name': "Dokumentation",
        'url': '',
        'is_active': False
    })
    breadcrumbs[-1]['is_active'] = True
    context = {
        'page': page,
        'breadcrumbs': breadcrumbs,
        'content': content,
    }
    return render(request, 'docs/read_page.html', context=context)


@login_required
def update_page(request, page):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            file = ContentFile(form.cleaned_data['content'], name=page + '.md')
            storage.save(name=file.name, content=file)
            return HttpResponseRedirect(reverse('docs:read_page', args=(page,)))
    else:
        content = storage.open(page + '.md').read().decode('utf-8')
        form = PageForm(initial={'title': page.replace('_', ' '), 'content': content})
    context = {
        'page': page,
        'title': page.replace('_', ' ').split('/')[-1],
        'form': form,
    }
    return render(request, 'docs/update_page.html', context=context)


@login_required
def delete_page(request, page):
    if request.method == 'POST':
        storage.delete(page + '.md')
        messages.add_message(request, messages.SUCCESS, f'Die Seite "{page}" wurde erfolgreich gelöscht.')
        return HttpResponseRedirect(reverse('docs:list_pages'))
    else:
        return HttpResponse(status=204)
