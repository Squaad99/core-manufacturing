from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from products.models import Product
from users.models import Company


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titel")
    comment = models.TextField(max_length=500, default="", verbose_name="Kommentar", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class ProductForProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    quantity = models.IntegerField(default=0, verbose_name="Antal")

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.product.id})
