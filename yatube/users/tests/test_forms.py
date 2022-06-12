from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class UserCreateFormTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_user_create(self):
        users_count = User.objects.count()
        form_data = {
            'username': 'test_user',
            'password1': 'UserCheck_56',
            'password2': 'UserCheck_56'
        }
        self.guest_client.post(
            reverse('users:signup'),
            data=form_data
        )
        self.assertEqual(users_count + 1, User.objects.count())
