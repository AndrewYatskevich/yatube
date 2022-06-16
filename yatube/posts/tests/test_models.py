from django.test import TestCase

from ..models import Group, Post, User, Comment, Follow

GROUP_SLUG = 'test-slug'
USER_USERNAME = 'TestName'
POST_AUTHOR_USERNAME = 'TestPostAuthor'
COMMENT_AUTHOR_USERNAME = 'TestCommentAuthor'
POST_TEXT = 'Тестовый текст'
COMMENT_TEXT = 'Текст комментария'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.post_author = User.objects.create_user(
            username=POST_AUTHOR_USERNAME
        )
        cls.comment_author = User.objects.create_user(
            username=COMMENT_AUTHOR_USERNAME
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=GROUP_SLUG,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.post_author,
            text=POST_TEXT,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.comment_author,
            text=COMMENT_TEXT
        )
        cls.follow = Follow.objects.create(
            user=cls.comment_author,
            author=cls.post_author
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_str = PostModelTest.post.__str__()
        self.assertEqual(post_str, PostModelTest.post.text[:15])

        group_str = PostModelTest.group.__str__()
        self.assertEqual(group_str, PostModelTest.group.title)

        comment_str = PostModelTest.comment.__str__()
        self.assertEqual(comment_str, PostModelTest.comment.text[:15])

        follow_str = PostModelTest.follow.__str__()
        self.assertEqual(
            follow_str,
            (f'Пользователь {COMMENT_AUTHOR_USERNAME}'
             f' подписан на пользователя {POST_AUTHOR_USERNAME}')
        )

    def test_post_model_have_correct_verbose_name(self):
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
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_group_model_have_correct_verbose_name(self):
        """Проверяем корректность verbose_name"""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Ссылка',
            'description': 'Описание',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_comment_model_have_correct_verbose_name(self):
        """Проверяем корректность verbose_name"""
        comment = PostModelTest.comment
        field_verboses = {
            'text': 'Текст комментария',
            'created': 'Дата комментария',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_post_model_have_correct_help_text(self):
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
