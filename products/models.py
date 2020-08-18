from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from company.models import WorkType
from materials.models import Material
from users.models import Company


class Product(models.Model):
    # Standard Fields
    title = models.CharField(max_length=100, verbose_name="Titel")
    comment = models.TextField(max_length=500, default="", verbose_name="Anteckning", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Specific Fields
    specification = models.TextField(max_length=500, default="", verbose_name="Specification", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


class WorkTaskForProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    work_hours = models.FloatField(max_length=20, default=0)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.product.id})


class MaterialForProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    units = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.product.id})
