from django.db import models

# Create your models here.
from company.models import Employee
from projects.models import Project
from users.models import Company


class TimeReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Projekt')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Anställd')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Företag')
    hours = models.FloatField(verbose_name='Timmar')
    date = models.DateField(verbose_name='Datum')


class WorkReport(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Företag')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Anställd')
    date = models.DateField(verbose_name='Datum')
    time_start = models.TimeField(verbose_name='Start')
    time_end = models.TimeField(verbose_name='Avslut')
