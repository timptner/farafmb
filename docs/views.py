import os

from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django_s3_storage.storage import S3Storage

from .forms import UpdateForm

storage = S3Storage(
    aws_region=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_s3_bucket_name=os.getenv('DO_SPACE_NAME_DOCS', 'farafmb-docs'),
    aws_s3_endpoint_url=os.getenv('DO_SPACE_ENDPOINT_URL_DOCS', 'https://fra1.digitaloceanspaces.com'),
    aws_s3_file_overwrite=True,
)


def list_pages(request):
    response = storage.s3_connection.list_objects_v2(Bucket=storage.settings.AWS_S3_BUCKET_NAME)
    files = []
    for entry in response.get('Contents', []):
        key = entry['Key'].rstrip('.md')
        files.append({'key': key, 'name': key.replace('_', ' ')})
    return render(request, 'docs/list_pages.html', {'files': files})


def read_page(request, resource):
    content = storage.open(resource + '.md').read().decode('utf-8')
    breadcrumbs = []
    for name in resource.split('/'):
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
        'resource': resource,
        'breadcrumbs': breadcrumbs,
        'content': content,
    }
    return render(request, 'docs/read_page.html', context=context)


def update_page(request, resource):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            file = ContentFile(form.cleaned_data['content'], name=resource + '.md')
            storage.save(name=file.name, content=file)
            return HttpResponseRedirect(reverse('docs:read_page', args=(resource,)))
    else:
        content = storage.open(resource + '.md').read().decode('utf-8')
        form = UpdateForm(initial={'title': resource.replace('_', ' '), 'content': content})
    context = {
        'resource': resource,
        'title': resource.replace('_', ' ').split('/')[-1],
        'form': form,
    }
    return render(request, 'docs/update_page.html', context=context)


def delete_page(request, resource):
    if request.method == 'POST':
        storage.delete(resource + '.md')
        messages.add_message(request, messages.SUCCESS, f'Die Seite "{resource}" wurde erfolgreich gelöscht.')
        return HttpResponseRedirect(reverse('docs:list_pages'))
    else:
        return HttpResponse(status=204)
