
from tasks.templatetags.tasks_extras import convert_smarkets_web_address_to_match_name
from tasks.models import Match, Task
from django.shortcuts import redirect, render


def view_task(request):
    matches = Match.objects.all()
    return render(request, 'task.html',
                  {'matches': matches})


def new_task(request):
    task = Task.objects.create()
    new_smarkets_event_address_text = request.POST[
        'smarkets_event_address_text']
    new_match_text = convert_smarkets_web_address_to_match_name(
        new_smarkets_event_address_text)
    Match.objects.create(text=new_match_text, task=task)
    return redirect('/tasks/the-only-task-in-the-world/')


def home_page(request):
    return render(request, 'home.html')
