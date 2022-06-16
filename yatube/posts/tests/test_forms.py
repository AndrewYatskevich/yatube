import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from ..models import Post, Group, User

UPLOADED_IMG = SimpleUploadedFile(
    name='small.gif',
    content=(
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    ),
    content_type='image/gif'
)
UPLOADED_TXT = SimpleUploadedFile(
    name='test.txt',
    content=(
        'Текст файла'.encode()
    ),
    content_type='text/plane'
)
POST_CREATE_URL = 'posts:post_create'
POST_EDIT_URL = 'posts:post_edit'
USER_USERNAME = 'TestName'
POST_AUTHOR_USERNAME = 'TestPostAuthor'
POST_TEXT = 'Тестовый текст'
GROUP_SLUG = 'test-slug'
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
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
            author=User.objects.create_user(username=POST_AUTHOR_USERNAME),
            group=Group.objects.get(slug=GROUP_SLUG)
        )
        cls.POST_ID = Post.objects.get(text=POST_TEXT).id

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client.force_login(self.user)
        self.post_author = Client()
        self.post_author.force_login(
            User.objects.get(username=POST_AUTHOR_USERNAME)
        )

    def test_post_create(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст 2',
            'image': UPLOADED_IMG,
        }
        form_data_with_wrong_img = {
            'text': 'Тестовый текст 3',
            'image': UPLOADED_TXT,
        }
        self.authorized_client.post(
            reverse(POST_CREATE_URL),
            data=form_data,
            follow=True
        )
        self.authorized_client.post(
            reverse(POST_CREATE_URL),
            data=form_data_with_wrong_img,
            follow=True
        )
        self.assertEqual(posts_count + 1, Post.objects.count())
        self.assertFalse(
            Post.objects.filter(text='Тестовый текст 3').exists()
        )
        self.assertEqual(
            Post.objects.first().text,
            'Тестовый текст 2'
        )

    def test_post_edit(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Измененный текст',
        }
        self.post_author.post(
            reverse(
                POST_EDIT_URL, kwargs={
                    'post_id': PostCreateFormTests.POST_ID
                }
            ),
            data=form_data,
            follow=True
        )
        self.assertEqual(posts_count, Post.objects.count())
        self.assertTrue(Post.objects.get(text='Измененный текст'))
