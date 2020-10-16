from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile


class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_users = 5
        for user_num in range(number_of_users):
            User.objects.create(
                username=f'Test{user_num}',
            )

    def test_lists_users(self):
        response = self.client.get(reverse('userList'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)