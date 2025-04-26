from django.test import TestCase

from task_manager.labels.forms import LabelForm
from task_manager.utils import get_test_label_data


class LabelFormTest(TestCase):
    fixtures = ["labels.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_label_data()

    def test_label_form_valid_data(self):
        label_form = LabelForm(data=self.test_data['new'])
        self.assertTrue(label_form.is_valid())
        self.assertEqual(label_form.errors, {})

    def test_label_form_duplicate_name(self):
        label_form = LabelForm(data=self.test_data['duplicated'])
        self.assertFalse(label_form.is_valid())
        self.assertEqual(
            label_form.errors,
            {'name': ['Label с таким Имя уже существует.']}
        )

    def test_label_form_empty_fields(self):
        data = self.test_data['new'].copy()
        data['name'] = ''
        label_form = LabelForm(data=data)
        self.assertFalse(label_form.is_valid())
        self.assertEqual(
            label_form.errors,
            {
                'name': ['Обязательное поле.'],
             }
        )

