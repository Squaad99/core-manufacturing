from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from materials.models import Material


class Product(models.Model):
    # Standard Fields
    title = models.CharField(max_length=100, verbose_name="Titel")
    comment = models.TextField(max_length=500, default="", verbose_name="Kommentar", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    # Specific Fields
    extra_cost = models.FloatField(max_length=20, verbose_name="Extra kostnad", default=0, blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return reverse('product-overview')


class WorkTask(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    work_hours = models.FloatField(max_length=20, default=0)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.product.id})


class MaterialForProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    units = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.product.id})
