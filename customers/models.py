from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titel")
    web_address = models.URLField(max_length=250, blank=True, verbose_name="Webbsida", default="")

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class ContactPerson(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.customer.id})
