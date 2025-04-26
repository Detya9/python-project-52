from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.utils import get_test_label_data


class TestLabelListView(TestCase):
    fixtures = ["users.json", "labels.json"]
    labels_quantity = 4

    def test_list_view_with_not_logged(self):
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_list_view_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertEqual(Label.objects.count(), self.labels_quantity)


class TestLabelCreateView(TestCase):
    fixtures = ["users.json", "labels.json"]
    labels_quantity = 4

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_label_data()

    def test_get_label_creation_with_not_logged(self):
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_label_creation_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_label_creation(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        new_label = self.test_data['new']
        response = self.client.post(reverse('label_create'), new_label)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        self.assertEqual(Label.objects.count(), self.labels_quantity + 1)


class TestLabelUpdateView(TestCase):
    fixtures = ["users.json", "labels.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_label_data()

    def test_label_update_with_not_logged(self):
        response = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_label_update_with_logged_in(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_label_update_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        updated_label = self.test_data['updated']
        response = self.client.post(reverse('label_update', kwargs={'pk': 1}),
                                    updated_label)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        updated_label1 = Label.objects.get(pk=1)
        self.assertEqual(updated_label1.name, updated_label["name"])


class TestLabelDeleteView(TestCase):
    fixtures = ["users.json", "labels.json"]
    labels_quantity = 4

    def test_label_delete_with_not_logged(self):
        response = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_label_delete_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_post_label_delete_with_logged_in(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.post(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=1)
        self.assertEqual(Label.objects.count(), self.labels_quantity - 1)

