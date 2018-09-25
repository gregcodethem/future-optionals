from tasks.models import Match, Task
from django.test import TestCase
from .views import convert_smarkets_web_address_to_match_name
from tasks.templatetags.tasks_extras import convert_smarkets_web_address_to_datetime_date_format
from datetime import date

SMARKETS_EVENT_ADDRESS_BASE = ('https://smarkets.com/event/956523/'
                               'sport/football/spain-la-liga/2018/09/23/')
SMARKETS_EVENT_ADDRESS_SAMPLE = ('https://smarkets.com/event/956523/'
                                 'sport/football/spain-la-liga/2018/09/23/'
                                 'fc-barcelona-vs-girona-fc')


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_smarkets_event_web_address_converted_to_match_name(self):

        smarkets_event_address_text = SMARKETS_EVENT_ADDRESS_SAMPLE

        match_name = convert_smarkets_web_address_to_match_name(
            smarkets_event_address_text)
        self.assertEqual(match_name, 'fc-barcelona-vs-girona-fc')

    def test_smarkets_event_web_address_returns_empty_string_from_empty_string_arg(self):
        match_name_empty_string = convert_smarkets_web_address_to_match_name(
            '')
        self.assertEqual(match_name_empty_string, '')

    def test_smarkets_event_web_address_returns_date_format(self):
        smarkets_event_address_text = SMARKETS_EVENT_ADDRESS_SAMPLE

        match_date = convert_smarkets_web_address_to_datetime_date_format(
            smarkets_event_address_text)
        self.assertEqual(date(2018, 9, 23), match_date)

    def test_does_not_return_entire_web_address_in_html(self):
        smarkets_event_address_text = SMARKETS_EVENT_ADDRESS_SAMPLE
        response = self.client.post(
            '/', data={'smarkets_event_address_text':
                       smarkets_event_address_text})
        self.assertNotIn(smarkets_event_address_text,
                         response.content.decode(),
                         'smarkets_event_address_text found in html response')

    def test_only_saves_matches_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Match.objects.count(), 0)


class TaskAndMatchModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        task = Task()
        task.save()

        first_match = Match()
        first_match.text = 'The first match'
        first_match.task = task
        first_match.save()

        second_match = Match()
        second_match.text = 'The second match'
        second_match.task = task
        second_match.save()

        saved_task = Task.objects.first()
        self.assertEqual(saved_task, task)

        saved_matches = Match.objects.all()
        self.assertEqual(saved_matches.count(), 2)

        first_saved_match = saved_matches[0]
        second_saved_match = saved_matches[1]
        self.assertEqual(first_saved_match.text, 'The first match')
        self.assertEqual(first_saved_match.task, task)
        self.assertEqual(second_saved_match.text, 'The second match')
        self.assertEqual(second_saved_match.task, task)


class TaskViewTest(TestCase):

    def test_passes_correct_task_to_template(self):
        other_task = Task.objects.create()
        correct_task = Task.objects.create()
        response = self.client.get(f'/tasks/{correct_task.id}/')
        self.assertEqual(response.context['task'], correct_task)

    def test_uses_task_template(self):
        task = Task.objects.create()
        response = self.client.get(
            f'/tasks/{task.id}/')
        self.assertTemplateUsed(response, 'task.html')

    def test_displays_only_matches_for_that_task(self):
        correct_task = Task.objects.create()
        Match.objects.create(text='match 1', task=correct_task)
        Match.objects.create(text='match 2', task=correct_task)

        other_task = Task.objects.create()
        Match.objects.create(text='other task match 1', task=other_task)
        Match.objects.create(text='other task match 2', task=other_task)

        response = self.client.get(f'/tasks/{correct_task.id}/')

        self.assertContains(response, 'match 1')
        self.assertContains(response, 'match 2')
        self.assertNotContains(response, 'other task match 1')
        self.assertNotContains(response, 'other task match 2')

    def test_displays_date_of_match(self):
        task = Task.objects.create()
        Match.objects.create(text='match 1', date="2018-09-23",
                             task=task)
        response = self.client.get(f'/tasks/{task.id}/')
        self.assertContains(response, '2018/09/23')


class NewTaskTest(TestCase):

    def test_can_save_date_of_match(self):
        self.client.post('/tasks/new',
                         data={'smarkets_event_address_text':
                               SMARKETS_EVENT_ADDRESS_SAMPLE})
        new_match = Match.objects.first()
        self.assertEqual(new_match.date, date(2018, 9, 23))

    def test_can_save_a_POST_request(self):
        self.client.post(
            '/tasks/new',
            data={'smarkets_event_address_text':
                  SMARKETS_EVENT_ADDRESS_BASE + 'A new match'})
        self.assertEqual(Match.objects.count(), 1)
        new_match = Match.objects.first()
        self.assertEqual(new_match.text, 'A new match')

    def test_redirects_after_POST_request(self):
        response = self.client.post(
            '/tasks/new',
            data={'smarkets_event_address_text':
                  SMARKETS_EVENT_ADDRESS_BASE + 'A new match'})
        new_task = Task.objects.first()
        self.assertRedirects(response,
                             f'/tasks/{new_task.id}/')


class NewMatchTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_task(self):
        other_task = Task.objects.create()
        correct_task = Task.objects.create()

        self.client.post(
            f'/tasks/{correct_task.id}/add_match',
            data={'smarkets_event_address_text':
                  SMARKETS_EVENT_ADDRESS_BASE + 'A new match for an existing task'}
        )

        self.assertEqual(Match.objects.count(), 1)
        new_match = Match.objects.first()
        self.assertEqual(new_match.text, 'A new match for an existing task')
        self.assertEqual(new_match.task, correct_task)

    def test_redirects_to_task_view(self):
        other_task = Task.objects.create()
        correct_task = Task.objects.create()

        response = self.client.post(
            f'/tasks/{correct_task.id}/add_match',
            data={'smarkets_event_address_text':
                  SMARKETS_EVENT_ADDRESS_BASE + 'A new match for an existing task'}
        )

        self.assertRedirects(response, f'/tasks/{correct_task.id}/')
