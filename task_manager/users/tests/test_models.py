from django.db.utils import IntegrityError
from django.test import TestCase

from task_manager.users.models import User
from task_manager.utils import get_test_user_data


class UserModelTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_user_data()

    def test_create_user(self):
        user = User.objects.create_user(
            first_name=self.test_data["new"]["first_name"],
            last_name=self.test_data["new"]["last_name"],
            username=self.test_data["new"]["username"],
            password=self.test_data["new"]["password1"])

        self.assertEqual(user.first_name, self.test_data["new"]["first_name"])
        self.assertEqual(user.last_name, self.test_data["new"]["last_name"])
        self.assertEqual(user.username, self.test_data["new"]["username"])
        self.assertTrue(user.check_password(self.test_data["new"]["password1"]))
        self.assertEqual(user.__str__(), self.test_data["new"]["first_name"]
                         + ' ' + self.test_data["new"]["last_name"])

    def test_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                first_name=self.test_data["duplicated"]["first_name"],
                last_name=self.test_data["duplicated"]["last_name"],
                username=self.test_data["duplicated"]["username"],
                password=self.test_data["duplicated"]["password1"])

