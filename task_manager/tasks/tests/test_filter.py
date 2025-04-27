from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class FilterTest(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json", "labels.json"]

    def test_status_case(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=2)
        result = list(Task.objects.filter(status=status))
        response = self.client.get(reverse('task_list') + "?status=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks']), result)

    def test_executor_case(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        result = list(Task.objects.filter(executor=user))
        response = self.client.get(reverse('task_list') + "?executor=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks']), result)

    def test_label_case(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=1)
        result = list(Task.objects.filter(labels=label))
        response = self.client.get(reverse('task_list') + "?label=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks']), result)

    def test_self_author_case(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        result = list(Task.objects.filter(author=user))
        response = self.client.get(reverse('task_list') + "?self_tasks=on")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks']), result)

    def test_multi_filter_case(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=1)
        status = Status.objects.get(pk=2)
        result = list(Task.objects.filter(labels=label).filter(status=status))
        response = self.client.get(reverse('task_list') + "?status=2&label=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['tasks']), result)

