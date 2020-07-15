from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from company.models import ProjectState, Company
from customers.models import Customer
from products.models import Product


class Project(models.Model):
    title = models.CharField(max_length=100,)
    comment = models.TextField(max_length=500, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Specific
    state = models.ForeignKey(ProjectState, on_delete=models.SET("Missing"))
    customer = models.ForeignKey(Customer, on_delete=models.SET("Missing"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class ProductForProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    quantity = models.IntegerField(default=0, verbose_name="Antal")

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.id})
