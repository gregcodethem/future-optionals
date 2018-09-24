from django.db import models


class Match(models.Model):
    text = models.TextField(default='')
