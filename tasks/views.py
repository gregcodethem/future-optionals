
from tasks.templatetags.tasks_extras import convert_smarkets_web_address_to_match_name
from tasks.models import Match
from django.shortcuts import render


def home_page(request):
    match = Match()
    smarkets_event_address_text = request.POST.get(
        'smarkets_event_address_text', '')
    match.text = convert_smarkets_web_address_to_match_name(
        smarkets_event_address_text)
    match.save()

    return render(request, 'home.html',
                  {'smarkets_event_address_text':
                   match.text})
