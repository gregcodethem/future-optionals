from django.test import TestCase
from .views import convert_smarkets_web_address_to_match_name


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post(
            '/', data={'smarkets_event_address_text': 'A new item'})
        self.assertIn('A new item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    def test_smarkets_event_web_address_converted_to_match_name(self):
        smarkets_event_address_text = ('https://smarkets.com/'
                                       'event/956523/sport/football/'
                                       'spain-la-liga/2018/09/23/'
                                       'fc-barcelona-vs-girona-fc')
        match_name = convert_smarkets_web_address_to_match_name(
            smarkets_event_address_text)
        self.assertEqual(match_name, 'fc-barcelona-vs-girona-fc')

    def test_does_not_return_entire_web_address_in_html(self):
        smarkets_event_address_text = ('https://smarkets.com/'
                                       'event/956523/sport/football/'
                                       'spain-la-liga/2018/09/23/'
                                       'fc-barcelona-vs-girona-fc')
        response = self.client.post(
            '/', data={'smarkets_event_address_text':
                       smarkets_event_address_text})
        self.assertNotIn(smarkets_event_address_text,
                         response.content.decode(),
                         'smarkets_event_address_text found in html response')
