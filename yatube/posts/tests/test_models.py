from django.test import TestCase

from ..models import Group, Post, User

GROUP_SLUG = 'test-slug'
USER_USERNAME = 'TestName'
POST_TEXT = 'Тестовый текст'
POST_AUTHOR_USERNAME = 'TestPostAuthor'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=GROUP_SLUG,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_str = PostModelTest.post.__str__()
        self.assertEqual(post_str, PostModelTest.post.text[:15])

        group_str = PostModelTest.group.__str__()
        self.assertEqual(group_str, PostModelTest.group.title)

    def test_model_have_correct_verbose_name(self):
        """Проверяем корректность verbose_name"""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_model_have_correct_help_text(self):
        """Проверяем корректность verbose_name"""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
