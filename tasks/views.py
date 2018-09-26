
from .utils import convert_smarkets_web_address_to_match_name
from .utils import convert_smarkets_web_address_to_datetime_date_format
from django.core.exceptions import ValidationError
from tasks.models import Match, Task
from django.shortcuts import redirect, render


def view_task(request, task_id):
    task = Task.objects.get(id=task_id)
    error = None

    if request.method == 'POST':
        
        new_smarkets_event_address_text = request.POST[
            'smarkets_event_address_text']
        new_match_text = convert_smarkets_web_address_to_match_name(
            new_smarkets_event_address_text)
        new_match_date = convert_smarkets_web_address_to_datetime_date_format(
            new_smarkets_event_address_text)
        try:
            match = Match.objects.create(text=new_match_text,
                                         date=new_match_date,
                                         task=task)
            match.full_clean()
            match.save()
            return redirect(f'/tasks/{task.id}/')
        except ValidationError:
            error = "You can't have an empty Smarkets event address"

    return render(request, 'task.html',
                  {'task': task, 'error': error})


def new_task(request):
    task = Task.objects.create()
    new_smarkets_event_address_text = request.POST[
        'smarkets_event_address_text']
    new_match_text = convert_smarkets_web_address_to_match_name(
        new_smarkets_event_address_text)
    new_match_date = convert_smarkets_web_address_to_datetime_date_format(
        new_smarkets_event_address_text)
    try:
        match = Match.objects.create(text=new_match_text,
                                     date=new_match_date,
                                     task=task)
        match.full_clean()
    except ValidationError:
        error = "You can't have an empty Smarkets event address"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/tasks/{task.id}/')


def home_page(request):
    return render(request, 'home.html')
