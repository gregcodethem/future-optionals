from datetime import date

def convert_smarkets_web_address_to_datetime_date_format(
        smarkets_event_address_text):
    event_information_list = smarkets_event_address_text.split('/')
    if len(event_information_list) == 1:
        return ''
    day = int(event_information_list[-2])
    month = int(event_information_list[-3])
    year = int(event_information_list[-4])
    return date(year, month, day)


def convert_smarkets_web_address_to_match_name(
        smarkets_event_address_text):
    event_information_list = smarkets_event_address_text.split('/')
    match_name = event_information_list[-1]
    return match_name