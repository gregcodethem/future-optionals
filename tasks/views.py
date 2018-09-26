
from .utils import convert_smarkets_web_address_to_match_name
from .utils import convert_smarkets_web_address_to_datetime_date_format
from django.core.exceptions import ValidationError
from tasks.forms import MatchForm
from tasks.models import Match, Task
from django.shortcuts import redirect, render


def view_task(request, task_id):
    task = Task.objects.get(id=task_id)
    form = MatchForm()

    if request.method == 'POST':
        form = MatchForm(data=request.POST)
        if form.is_valid():

            new_smarkets_event_address_text = request.POST[
                'text']
            new_match_text = convert_smarkets_web_address_to_match_name(
                new_smarkets_event_address_text)
            new_match_date = convert_smarkets_web_address_to_datetime_date_format(
                new_smarkets_event_address_text)

            Match.objects.create(text=new_match_text,
                                 date=new_match_date,
                                 task=task)

            return redirect(task)

    return render(request, 'task.html',
                  {'task': task, "form": form})


def new_task(request):
    form = MatchForm(data=request.POST)
    if form.is_valid():
        task = Task.objects.create()
        new_smarkets_event_address_text = request.POST[
            'text']
        new_match_text = convert_smarkets_web_address_to_match_name(
            new_smarkets_event_address_text)
        new_match_date = convert_smarkets_web_address_to_datetime_date_format(
            new_smarkets_event_address_text)
        Match.objects.create(text=new_match_text,
                             date=new_match_date,
                             task=task)
        return redirect(task)
    else:
        return render(request, 'home.html', {"form": form})


def home_page(request):
    return render(request, 'home.html', {'form': MatchForm()})
