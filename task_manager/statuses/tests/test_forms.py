from django.test import TestCase

from task_manager.statuses.forms import StatusForm
from task_manager.utils import get_test_status_data


class StatusFormTest(TestCase):
    fixtures = ["statuses.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_status_data()

    def test_status_form_valid_data(self):
        status_form = StatusForm(data=self.test_data['new'])
        self.assertTrue(status_form.is_valid())
        self.assertEqual(status_form.errors, {})

    def test_status_form_duplicate_name(self):
        status_form = StatusForm(data=self.test_data['duplicated'])
        self.assertFalse(status_form.is_valid())
        self.assertEqual(
            status_form.errors,
            {'name': ['Status с таким Имя уже существует.']}
        )

    def test_status_form_empty_fields(self):
        data = self.test_data['new'].copy()
        data['name'] = ''
        status_form = StatusForm(data=data)
        self.assertFalse(status_form.is_valid())
        self.assertEqual(
            status_form.errors,
            {
                'name': ['Обязательное поле.'],
             }
        )

