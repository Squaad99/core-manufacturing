from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Company(models.Model):
    title = models.CharField(max_length=30)
    currency = models.CharField(max_length=10, default="SEK", verbose_name='Valuta')
    cost_per_work_hour = models.IntegerField(default=0, verbose_name='Kostnad per timma för arbete')

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return reverse('company-profile')


class Profile(models.Model):
    title = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class ProjectState(models.Model):
    title = models.CharField(max_length=30)
    index_position = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

