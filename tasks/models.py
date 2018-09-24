from django.db import models


class Task(models.Model):
    pass


class Match(models.Model):
    text = models.TextField(default='')
    task = models.ForeignKey(Task, default=None)
