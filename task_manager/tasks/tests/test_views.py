from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.utils import get_test_task_data


class TestTaskListView(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]
    tasks_quantity = 2

    def test_list_view_with_not_logged(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_list_view_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertEqual(Task.objects.count(), self.tasks_quantity)


class TestTaskDetailView(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]

    def test_detail_view_with_not_logged(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_list_view_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('task_info', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_info.html')


class TestTaskCreateView(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]
    tasks_quantity = 2

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_task_data()

    def test_get_task_creation_with_not_logged(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_task_creation_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_task_creation(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        new_task = self.test_data['new']
        response = self.client.post(reverse('task_create'), new_task)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), self.tasks_quantity + 1)


class TestTaskUpdateView(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_task_data()

    def test_task_update_with_not_logged(self):
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_task_update_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_task_update_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        updated_task = self.test_data['updated']
        response = self.client.post(reverse('task_update', kwargs={'pk': 1}),
                                    updated_task)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        updated_task1 = Task.objects.get(pk=1)
        self.assertEqual(updated_task1.name, updated_task["name"])
        self.assertEqual(updated_task1.description,
                         updated_task["description"])


class TestTaskDeleteView(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]
    task_quantity = 2

    def test_task_delete_with_not_logged(self):
        response = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_task_delete_with_another_user(self):
        user2 = User.objects.get(pk=2)
        self.client.force_login(user2)
        response = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))

    def test_get_task_delete_with_author(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_post_task_delete_with_author(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.post(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=1)
        self.assertEqual(Task.objects.count(), self.task_quantity - 1)

