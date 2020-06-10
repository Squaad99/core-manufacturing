from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Profile(models.Model):
    title = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
