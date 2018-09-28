from django.db import models
from datetime import date
from django.core.urlresolvers import reverse


class Task(models.Model):

    def get_absolute_url(self):
        return reverse('view_task', args=[self.id])


class Match(models.Model):
    text = models.TextField(default='')
    task = models.ForeignKey(Task, default=None)
    date = models.DateField(default=date.today)
    match_text = models.TextField(default='')
