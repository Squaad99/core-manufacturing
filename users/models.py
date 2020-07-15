from django.db import models
from django.contrib.auth.models import User

from company.models import Company


class Profile(models.Model):
    title = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
