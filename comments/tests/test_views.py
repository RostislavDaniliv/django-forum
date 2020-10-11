# from django.test import TestCase
# from rest_framework.test import APITestCase
# from rest_framework.test import APIRequestFactory
# from rest_framework import status
# from django.urls import reverse
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
#
#
# class AccountsTestCase(APITestCase):
#     def setUp(self):
#         self.test_user = User.objects.create_user('test_u', 'test@rengorum.com', 'anythingcanlah')
#         self.create_url = reverse('user-register')
#         self.detail_url = reverse('user-detail')
#
#     # def test_create_user(self):
#     #     data = {
#     #         'username': 'test_u',
#     #         'email': 'test_u@facebook.com',
#     #         'password': 'test_u'
#     #     }
#     #
#     #     response = self.client.post(self.create_url, data, format='json')
#     #     self.assertEqual(User.objects.count(), 1)
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #     self.assertEqual(response.data['username'], data['username'])
#     #     self.assertEqual(response.data['email'], data['email'])
#     #     self.assertFalse('password' in response.data)
#
#     def test_detail_user(self):
#         data = {
#             'id': '3',
#             'username': 'test_ban',
#             'name': 'TestBan Name',
#             'bio': 'TestBan bio',
#             'is_staff': 'False',
#         }
#
#         response = self.client.get(self.detail_url, data, format='json')
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(response.data['id'], data['id'])
#         self.assertEqual(response.data['username'], data['username'])
#         self.assertEqual(response.data['bio'], data['bio'])
#         self.assertEqual(response.data['is_staff'], data['is_staff'])
#
#
