
from .utils import convert_smarkets_web_address_to_match_name
from .utils import convert_smarkets_web_address_to_datetime_date_format
from tasks.models import Match, Task
from django.shortcuts import redirect, render


def add_match(request, task_id):
    task = Task.objects.get(id=task_id)
    new_smarkets_event_address_text = request.POST[
        'smarkets_event_address_text']
    new_match_text = convert_smarkets_web_address_to_match_name(
        new_smarkets_event_address_text)
    new_match_date = convert_smarkets_web_address_to_datetime_date_format(
        new_smarkets_event_address_text)
    Match.objects.create(text=new_match_text, date=new_match_date,
                         task=task)
    return redirect(f'/tasks/{task.id}/')


def view_task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'task.html',
                  {'task': task})


def new_task(request):
    task = Task.objects.create()
    new_smarkets_event_address_text = request.POST[
        'smarkets_event_address_text']
    new_match_text = convert_smarkets_web_address_to_match_name(
        new_smarkets_event_address_text)
    new_match_date = convert_smarkets_web_address_to_datetime_date_format(
        new_smarkets_event_address_text)
    Match.objects.create(text=new_match_text, date=new_match_date,
                         task=task)
    return redirect(f'/tasks/{task.id}/')


def home_page(request):
    return render(request, 'home.html')
