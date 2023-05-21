from django.db import models
from pathlib import Path


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"
        ordering = ['name']

    def __str__(self):
        return self.name


class Document(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    visible = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumente"
        ordering = ['title']

    def __str__(self):
        return self.title

    def file_suffix(self):
        return Path(self.file.name).suffix

    def icon(self):
        suffix = self.file_suffix()
        if suffix == '.pdf':
            return "fas fa-file-pdf"
        elif suffix == '.zip':
            return "fas fa-file-archive"
        else:
            return "fas fa-file"
