
from django.shortcuts import render


def convert_smarkets_web_address_to_match_name(smarkets_event_address_text):
    event_information_list = smarkets_event_address_text.split('/')
    match_name = event_information_list[-1]
    return match_name


def home_page(request):
    return render(request, 'home.html',
                  {'match_name':
                   request.POST.get('smarkets_event_address_text', '')})
