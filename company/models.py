from django.db import models

# Create your models here.
from django.urls import reverse


class Company(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateField(auto_now_add=True)
    currency = models.CharField(max_length=10, default="SEK", verbose_name='Valuta')
    cost_per_work_hour = models.IntegerField(default=0, verbose_name='Kostnad per timma för arbete')

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return reverse('company-profile')


class Employee(models.Model):
    title = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectState(models.Model):
    title = models.CharField(max_length=30)
    index_position = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
