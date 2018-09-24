from django import template

register = template.Library()


def convert_smarkets_web_address_to_match_name(smarkets_event_address_text):
    event_information_list = smarkets_event_address_text.split('/')
    match_name = event_information_list[-1]
    return match_name
