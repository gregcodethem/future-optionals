from django.core.exceptions import ValidationError
from tasks.models import Match, Task
from django.test import TestCase


class TaskAndMatchModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        task = Task()
        task.save()

        first_match = Match()
        first_match.full_text = 'The first match'
        first_match.task = task
        first_match.save()

        second_match = Match()
        second_match.full_text = 'The second match'
        second_match.task = task
        second_match.save()

        saved_task = Task.objects.first()
        self.assertEqual(saved_task, task)

        saved_matches = Match.objects.all()
        self.assertEqual(saved_matches.count(), 2)

        first_saved_match = saved_matches[0]
        second_saved_match = saved_matches[1]
        self.assertEqual(first_saved_match.full_text, 'The first match')
        self.assertEqual(first_saved_match.task, task)
        self.assertEqual(second_saved_match.full_text, 'The second match')
        self.assertEqual(second_saved_match.task, task)

    def test_cannot_save_empty_text_task_matches(self):
        task = Task.objects.create()
        match = Match(task=task, full_text='')
        with self.assertRaises(ValidationError):
            match.save()
            match.full_clean()

    def test_cannot_save_empty_date_task_matches(self):
        task = Task.objects.create()
        match = Match(task=task, date='')
        with self.assertRaises(ValidationError):
            match.save()
            match.full_clean()

    def test_get_absolute_url(self):
        task = Task.objects.create()
        self.assertEqual(task.get_absolute_url(),
                         f'/tasks/{task.id}/')
