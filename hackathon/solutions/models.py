from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class FileItem(models.Model):
    user                            = models.ForeignKey(get_user_model(), default=1, on_delete=models.)
    name                            = models.CharField(max_length=120, null=True, blank=True)
    path                            = models.TextField(blank=True, null=True)
    size                            = models.BigIntegerField(default=0)
    file_type                       = models.CharField(max_length=120, null=True, blank=True)
    timestamp                       = models.DateTimeField(auto_now_add=True)
    updated                         = models.DateTimeField(auto_now=True)
    uploaded                        = models.BooleanField(default=False)
    active                          = models.BooleanField(default=True)

    @property
    def title(self):
        return str(self.name)
