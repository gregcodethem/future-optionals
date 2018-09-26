from django.test import TestCase

from tasks.forms import EMPTY_INPUT_ERROR, MatchForm


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
            form.errors['text'],
            [EMPTY_INPUT_ERROR]
        )
