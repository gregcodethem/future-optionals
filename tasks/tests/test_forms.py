from django.test import TestCase

from tasks.forms import EMPTY_INPUT_ERROR, MatchForm
from tasks.models import Match, Task

DUMMY_ADDRESS = ('https://smarkets.com/event/957448/'
                  'sport/football/league-cup/2018/09/26/'
                  'tottenham-vs-watford-fc')

class ItemFormTest(TestCase):

    def test_form_match_input_has_placeholder(self):
        form = MatchForm()
        self.assertIn(
            'placeholder="Enter a Smarkets event web address"',
            form.as_p())

    def test_form_validation_for_blank_items(self):
        form = MatchForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['full_text'],
            [EMPTY_INPUT_ERROR]
        )

    def test_form_save_handles_saving_to_a_task(self):
        task = Task.objects.create()
        form = MatchForm(
            data={'full_text':
                  DUMMY_ADDRESS})
        new_match = form.save(for_task=task,
                              full_text=DUMMY_ADDRESS)
        self.assertEqual(new_match, Match.objects.first())
