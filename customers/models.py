from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from company.models import Company


class Customer(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titel")
    comment = models.TextField(max_length=500, default="", verbose_name="Anteckning", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Customer specific
    web_address = models.URLField(max_length=100, verbose_name="Websida", blank=True)

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class ContactPerson(models.Model):
    name = models.CharField(max_length=30, verbose_name="Namn")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(max_length=50, verbose_name="Email")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.customer.id})
