from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Post, Group, User

GROUP_SLUG = 'test-slug'
USER_USERNAME = 'TestName'
POST_TEXT = 'Тестовый текст'
POST_AUTHOR_USERNAME = 'TestPostAuthor'


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовый заголовок',
            slug=GROUP_SLUG,
            description='Тестовое описание'
        )
        Post.objects.create(
            text=POST_TEXT,
            author=User.objects.create_user(username=POST_AUTHOR_USERNAME)
        )
        cls.POST_ID = Post.objects.get(text=POST_TEXT).id

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_author = Client()
        self.post_author.force_login(
            User.objects.get(username=POST_AUTHOR_USERNAME)
        )

    def test_templates_and_urls_available_to_all_users(self):
        """Страницы с корректными шаблонами, доступные всем пользователям"""
        url_template_names = {
            '/': 'posts/index.html',
            f'/group/{GROUP_SLUG}/': 'posts/group_list.html',
            f'/profile/{USER_USERNAME}/': 'posts/profile.html',
            f'/posts/{PostsURLTests.POST_ID}/': 'posts/post_detail.html',
        }
        for address, template in url_template_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_templates_and_urls_available_to_authorized_users(self):
        """Страницы с корректными шаблонами, доступные авторизованным
        пользователям """
        url_template_names = {
            '/create/': 'posts/create_post.html',
        }
        for address, template in url_template_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_templates_and_urls_available_to_post_author(self):
        """Страницы с корректными шаблонами, доступные автору поста """
        url_template_names = {
            f'/posts/{PostsURLTests.POST_ID}/edit/': 'posts/create_post.html',
        }
        for address, template in url_template_names.items():
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_unexisting_url(self):
        """Проверка несуществующей страницы"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
