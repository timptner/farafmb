from django.db import models
from pathlib import Path


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    visible = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.title
