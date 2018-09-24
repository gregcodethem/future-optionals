
from tasks.templatetags.tasks_extras import convert_smarkets_web_address_to_match_name
from tasks.models import Match
from django.shortcuts import redirect, render


def home_page(request):
    if request.method == 'POST':
        new_smarkets_event_address_text = request.POST[
            'smarkets_event_address_text']
        new_match_text = convert_smarkets_web_address_to_match_name(
            new_smarkets_event_address_text)
        Match.objects.create(text=new_match_text)
        return redirect('/')
    return render(request, 'home.html')
