from django.contrib.auth.models import User
from django.db import models


class CommonObjectValues(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)