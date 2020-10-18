from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile


class UserRegisterTest(TestCase):

    def test_registration_view(self):
        response = self.client.post(reverse('userRegister'),
                                    data={'username': 'TestReg',
                                          'password': '127896354Aa',
                                          'Name': 'TestName',
                                          'email': 'test@mail.com',
                                          'bio': 'bio Test',
                                          })
        self.assertEqual(response.reason_phrase, 'Created')
        self.assertEqual(response.status_code, 201)


class UserLoginTest(TestCase):

    @classmethod
    def setUp(self):
        test_user = User.objects.create_user(username='testLogin', password='127896354Aa')
        test_user.save()

    def test_login_user(self):
        login = {'username':'testLogin', 'password':'127896354Aa'}
        response = self.client.post(reverse('userLogin'), login)
        self.assertEqual(str(response.data['username']), 'testLogin')
        self.assertEqual(response.status_code, 200)


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


class UserDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='TestDelete',
            is_staff='True',
        )

    def test_lists_users(self):
        user = User.objects.get(username='TestDelete')
        response = self.client.delete(reverse('userDelete', args=(user.username,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.status_text, 'No Content')


class UserUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='TestUpdate',
        )

    def test_update_users(self):
        user = User.objects.get(username='TestUpdate')
        response = self.client.put(reverse('userUpdate', args=(user.username,),),
                                   data={
                                       'name': 'EditName',
                                       'email': 'edit@mail.com',
                                       'bio': 'EditBio',


                                          })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'No Content')