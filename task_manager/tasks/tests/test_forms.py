from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.users.models import User
from task_manager.utils import get_test_task_data


class TaskFormTest(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json", "labels.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_task_data()
        data = cls.test_data['new']
        data['author'] = User.objects.get(pk=cls.test_data["new"]["author"])
        data['executor'] = User.objects.get(
            pk=cls.test_data["new"]["executor"])
        data['status'] = Status.objects.get(pk=cls.test_data["new"]["status"])

    def test_task_form_valid_data(self):
        data = self.test_data['new']
        task_form = TaskForm(data=data)
        self.assertTrue(task_form.is_valid())
        self.assertEqual(task_form.errors, {})

    def test_task_form_duplicate_name(self):
        task_form = TaskForm(data=self.test_data['duplicated'])
        self.assertFalse(task_form.is_valid())
        self.assertEqual(
            task_form.errors,
            {'name': ['Task с таким Имя уже существует.']}
        )

    def test_task_form_empty_fields(self):
        data = self.test_data['new'].copy()
        data['name'] = ''
        data['status'] = ''
        status_form = TaskForm(data=data)
        self.assertFalse(status_form.is_valid())
        self.assertEqual(
            status_form.errors,
            {
                'name': ['Обязательное поле.'],
                'status': ['Обязательное поле.'],
             }
        )

