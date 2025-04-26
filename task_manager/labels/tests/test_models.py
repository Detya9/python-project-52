from django.db.utils import IntegrityError
from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.utils import get_test_label_data


class LabelModelTest(TestCase):
    fixtures = ["labels.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_label_data()

    def test_create_label(self):
        label = Label.objects.create(
            name=self.test_data["new"]["name"],
        )

        self.assertEqual(label.name, self.test_data["new"]["name"])
        self.assertEqual(label.__str__(), self.test_data["new"]["name"])

    def test_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            Label.objects.create(
                name=self.test_data["duplicated"]["name"])

