from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.utils import get_test_status_data


class TestStatusListView(TestCase):
    fixtures = ["users.json", "statuses.json"]
    statuses_quantity = 4

    def test_list_view_with_not_logged(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_list_view_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertEqual(Status.objects.count(), self.statuses_quantity)


class TestStatusCreateView(TestCase):
    fixtures = ["users.json", "statuses.json"]
    statuses_quantity = 4

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_status_data()

    def test_get_status_creation_with_not_logged(self):
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_status_creation_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_status_creation(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        new_status = self.test_data['new']
        response = self.client.post(reverse('status_create'), new_status)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        self.assertEqual(Status.objects.count(), self.statuses_quantity + 1)


class TestStatusUpdateView(TestCase):
    fixtures = ["users.json", "statuses.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_status_data()

    def test_status_update_with_not_logged(self):
        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_status_update_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_status_update_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        updated_status = self.test_data['updated']
        response = self.client.post(reverse('status_update', kwargs={'pk': 1}),
                                    updated_status)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        updated_status1 = Status.objects.get(pk=1)
        self.assertEqual(updated_status1.name, updated_status["name"])


class TestStatusDeleteView(TestCase):
    fixtures = ["users.json", "statuses.json"]
    statuses_quantity = 4

    def test_status_delete_with_not_logged(self):
        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_status_delete_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_post_status_delete_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.post(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=1)
        self.assertEqual(Status.objects.count(), self.statuses_quantity - 1)

