from django.core.exceptions import ValidationError
from tasks.models import Match, Task
from django.test import TestCase


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

    def test_cannot_save_empty_task_matches(self):
        task = Task.objects.create()
        match = Match(task=task, text='')
        with self.assertRaises(ValidationError):
            match.save()
            match.full_clean()
