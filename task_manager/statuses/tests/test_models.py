from django.db.utils import IntegrityError
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.utils import get_test_status_data


class StatusModelTest(TestCase):
    fixtures = ["statuses.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_status_data()

    def test_create_status(self):
        status = Status.objects.create(
            name=self.test_data["new"]["name"],
        )

        self.assertEqual(status.name, self.test_data["new"]["name"])
        self.assertEqual(status.__str__(), self.test_data["new"]["name"])

    def test_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            Status.objects.create(
                name=self.test_data["duplicated"]["name"])

