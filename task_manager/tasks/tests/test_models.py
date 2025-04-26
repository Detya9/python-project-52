from django.db.utils import IntegrityError
from django.test import TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.utils import get_test_task_data


class TaskModelTest(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_task_data()

    def test_create_task(self):
        author = User.objects.get(pk=self.test_data["new"]["author"])
        status = Status.objects.get(pk=self.test_data["new"]["status"])
        executor = User.objects.get(pk=self.test_data["new"]["executor"])
        task = Task.objects.create(
            name=self.test_data["new"]["name"],
            description=self.test_data["new"]["description"],
            status=status,
            author=author,
            executor=executor,
        )

        self.assertEqual(task.name, self.test_data["new"]["name"])
        self.assertEqual(task.description,
                         self.test_data["new"]["description"])
        self.assertEqual(task.status, status)
        self.assertEqual(task.author, author)
        self.assertEqual(task.executor, executor)
        self.assertEqual(task.__str__(), self.test_data["new"]["name"])

    def test_duplicate_name(self):
        author = User.objects.get(pk=self.test_data["duplicated"]["author"])
        status = Status.objects.get(pk=self.test_data["duplicated"]["status"])
        with self.assertRaises(IntegrityError):
            Task.objects.create(
                name=self.test_data["duplicated"]["name"],
                author=author,
                status=status)

