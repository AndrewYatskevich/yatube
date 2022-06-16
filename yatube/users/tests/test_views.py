from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class UsersPagesTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username='TestName',
            password='H_1_N'
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = (
            (reverse('users:signup'), 'users/signup.html'),
            (reverse('users:login'), 'users/login.html'),
            (reverse('users:password_change'),
                'users/password_change_form.html'),
            (reverse('users:password_change_done'),
                'users/password_change_done.html'),
            (reverse('users:password_reset'),
             'users/password_reset_form.html'),
            (reverse('users:password_reset_done'),
                'users/password_reset_done.html'),
            (reverse(
                'users:password_reset_confirm',
                args=('test_uidb64', 'test_token')
            ), 'users/password_reset_confirm.html'),
            (reverse('users:password_reset_complete'),
                'users/password_reset_complete.html'),
            (reverse('users:logout'), 'users/logged_out.html'),
        )
        for reverse_name, template in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_page_show_correct_context(self):
        """Шаблон signup сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('users:signup'))
        context_form = response.context['form']
        self.assertIsInstance(context_form, CreationForm)
