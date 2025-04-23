from django.test import TestCase

from task_manager.users.forms import CustomUserCreationForm
from task_manager.utils import get_test_user_data


class UserCreationFormTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_user_data()

    def test_user_form_valid_data(self):
        user_form = CustomUserCreationForm(data=self.test_data['new'])
        self.assertTrue(user_form.is_valid())
        self.assertEqual(user_form.errors, {})

    def test_user_form_password_missmatch(self):
        data = self.test_data['new'].copy()
        data['password2'] = 'missmatch'
        user_form = CustomUserCreationForm(data=data)
        self.assertFalse(user_form.is_valid())
        self.assertEqual(user_form.errors,
                         {'password2': ['Введенные пароли не совпадают.']}
                         )

    def test_user_form_duplicate_username(self):
        user_form = CustomUserCreationForm(data=self.test_data['duplicated'])
        self.assertFalse(user_form.is_valid())
        self.assertEqual(
            user_form.errors,
            {'username': ['Пользователь с таким именем уже существует.']}
        )

    def test_user_form_short_password(self):
        data = self.test_data['new'].copy()
        data['password1'] = '11'
        data['password2'] = '11'
        user_form = CustomUserCreationForm(data=data)
        self.assertFalse(user_form.is_valid())
        self.assertNotEqual(user_form.errors, {})

    def test_user_form_wrong_username(self):
        data = self.test_data['new'].copy()
        data['username'] = 'Bolgarin???'
        user_form = CustomUserCreationForm(data=data)
        self.assertFalse(user_form.is_valid())
        self.assertNotEqual(user_form.errors, {})

    def test_user_form_empty_fields(self):
        data = self.test_data['new'].copy()
        data['first_name'] = ''
        data['last_name'] = ''
        user_form = CustomUserCreationForm(data=data)
        self.assertFalse(user_form.is_valid())
        self.assertEqual(
            user_form.errors,
            {
                'first_name': ['Обязательное поле.'],
                'last_name': ['Обязательное поле.']
            }
        )

