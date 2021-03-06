from django.db import models
from datetime import date
from django.core.urlresolvers import reverse


class Task(models.Model):

    def get_absolute_url(self):
        return reverse('view_task', args=[self.id])


class Match(models.Model):
    full_text = models.TextField(default='')
    text = models.TextField(default='')
    task = models.ForeignKey(Task, default=None)
    date = models.DateField(default=date.today)
    amount_already_bet_home = models.FloatField(default=0)
    amount_already_bet_away = models.FloatField(default=0)

