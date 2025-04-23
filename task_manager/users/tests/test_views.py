from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User
from task_manager.utils import get_test_user_data


class TestUserListView(TestCase):
    fixtures = ["users.json"]
    users_quantity = 2

    def test_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(User.objects.count(), self.users_quantity)


class TestUserCreateView(TestCase):
    fixtures = ["users.json"]
    users_quantity = 2

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_user_data()

    def test_get_user_creation(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_user_creation(self):
        new_user = self.test_data['new']
        response = self.client.post(reverse('registration'), new_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), self.users_quantity + 1)


class TestUserUpdateView(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_user_data()

    def test_user_update_with_not_logged(self):
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_with_other_user(self):
        user2 = User.objects.get(pk=2)
        self.client.force_login(user2)
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

    def test_get_user_update_with_himself(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('user_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_user_update_with_himself(self):
        user1 = User.objects.get(pk=1)
        updated_user = self.test_data['updated']
        self.client.force_login(user1)
        response = self.client.post(reverse('user_update', kwargs={'pk': 1}),
                                    updated_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        updated_user1 = User.objects.get(pk=1)
        self.assertEqual(updated_user1.username, updated_user["username"])
        self.assertEqual(updated_user1.first_name, updated_user["first_name"])
        self.assertTrue(updated_user1.check_password(updated_user["password1"]))


class TestUserDeleteView(TestCase):
    fixtures = ["users.json"]
    users_quantity = 2

    def test_user_delete_with_not_logged(self):
        response = self.client.get(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_delete_with_other_user(self):
        user2 = User.objects.get(pk=2)
        self.client.force_login(user2)
        response = self.client.get(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

    def test_get_user_delete_with_himself(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.get(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_post_user_delete_with_himself(self):
        user1 = User.objects.get(pk=1)
        self.client.force_login(user1)
        response = self.client.post(reverse('user_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=1)
        self.assertEqual(User.objects.count(), self.users_quantity - 1)

