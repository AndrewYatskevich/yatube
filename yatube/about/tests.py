from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

AUTHOR_URL = reverse('about:author')
TECH_URL = reverse('about:tech')


class AboutTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_available_to_all_users(self):
        """Страницы с корректными шаблонами, доступные всем пользователям"""
        url_template_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in url_template_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_pages_use_correct_template(self):
        templates_pages_names = {
            AUTHOR_URL: 'about/author.html',
            TECH_URL: 'about/tech.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_author_page_accessible_by_name(self):
        response = self.guest_client.get(AUTHOR_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_page_accessible_by_name(self):
        response = self.guest_client.get(TECH_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
