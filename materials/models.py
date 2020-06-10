from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from users.models import Company


class Material(models.Model):
    # Standard Fields
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Class specific
    base_cost = models.FloatField(max_length=20)
    scalable_cost = models.BooleanField(default=False)
    unit_label = models.CharField(max_length=100, default="")
    unit_cost = models.FloatField(max_length=20)

    def get_absolute_url(self):
        return reverse('material-overview')

    def __str__(self):
        return self.title
