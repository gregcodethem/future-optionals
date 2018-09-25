from django.db import models
from datetime import date


class Task(models.Model):
    pass


class Match(models.Model):
    text = models.TextField(default='')
    task = models.ForeignKey(Task, default=None)
    date = models.DateField(default=date.today)
