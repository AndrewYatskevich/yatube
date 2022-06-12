import shutil
import tempfile

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Group, User, Comment
from ..forms import PostForm

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
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
GROUP_SLUG = 'test-slug'
POST_TEXT = 'Тестовый текст'
COMMENT_TEXT = 'Текст комментария'
POST_AUTHOR_USERNAME = 'TestPostAuthor'
COMMENT_AUTHOR_USERNAME = 'TestCommentAuthor'
USER_USERNAME = 'TestName'
INDEX_URL = reverse('posts:index')
GROUP_LIST_URL = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG})
PROFILE_URL = reverse(
    'posts:profile', kwargs={'username': POST_AUTHOR_USERNAME}
)
POST_CREATE_URL = reverse('posts:post_create')
POST_DETAIL_URL = 'posts:post_detail'
POST_EDIT_URL = 'posts:post_edit'
ADD_COMMENT_URL = 'posts:add_comment'


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
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
            group=Group.objects.get(slug=GROUP_SLUG),
            image=UPLOADED_IMG
        )
        Comment.objects.create(
            post=Post.objects.get(text=POST_TEXT),
            author=User.objects.create_user(username=COMMENT_AUTHOR_USERNAME),
            text=COMMENT_TEXT
        )
        cls.POST_ID = Post.objects.get(text=POST_TEXT).id

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            INDEX_URL: 'posts/index.html',
            GROUP_LIST_URL: 'posts/group_list.html',
            PROFILE_URL: 'posts/profile.html',
            POST_CREATE_URL: 'posts/create_post.html',
            reverse(
                POST_DETAIL_URL, kwargs={'post_id': PostsPagesTests.POST_ID}
            ): 'posts/post_detail.html',
            reverse(
                POST_EDIT_URL, kwargs={'post_id': PostsPagesTests.POST_ID}
            ): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом"""
        response = self.authorized_client.get(INDEX_URL)
        context_posts = list(response.context['page_obj'].object_list)
        all_posts = list(Post.objects.all())
        self.assertEqual(context_posts, all_posts)
        self.assertTrue(context_posts[0].image)

    def test_index_page_create_correct_cache(self):
        """Шаблон index создает корректный кэш"""
        cache.clear()
        post = Post.objects.create(
            text='ТестКэш',
            author=User.objects.get(username=POST_AUTHOR_USERNAME),
        )
        self.authorized_client.get(INDEX_URL)
        Post.objects.get(text='ТестКэш').delete()
        response_1 = self.authorized_client.get(INDEX_URL)
        self.assertTrue(post.text in response_1.content.decode())
        cache.clear()
        response_2 = self.authorized_client.get(INDEX_URL)
        self.assertFalse(post.text in response_2.content.decode())

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом"""
        response = self.authorized_client.get(GROUP_LIST_URL)
        context_posts = response.context['page_obj'].object_list
        all_group_posts = list(response.context['group'].posts.all())
        self.assertEqual(context_posts, all_group_posts)
        self.assertTrue(context_posts[0].image)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом"""
        response = self.authorized_client.get(PROFILE_URL)
        context_posts = response.context['page_obj'].object_list
        all_user_posts = list(response.context['author'].posts.all())
        self.assertEqual(context_posts, all_user_posts)
        self.assertTrue(context_posts[0].image)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse(
                POST_DETAIL_URL, kwargs={'post_id': PostsPagesTests.POST_ID}
            )
        )
        context_post = response.context['post']
        post_by_post_id = Post.objects.get(pk=PostsPagesTests.POST_ID)
        self.assertEqual(context_post, post_by_post_id)
        self.assertTrue(context_post.image)
        self.assertTrue(
            Comment.objects.get(text=COMMENT_TEXT)
            in response.context['comments']
        )

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом"""
        response = self.authorized_client.get(POST_CREATE_URL)
        context_form = response.context['form']
        self.assertIsInstance(context_form, PostForm)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse(POST_EDIT_URL, kwargs={'post_id': PostsPagesTests.POST_ID})
        )
        post = Post.objects.get(pk=response.context['post_id'])
        context_form = response.context['form']
        self.assertIsInstance(context_form, PostForm)
        self.assertEqual(context_form['text'].value(), post.text)
        self.assertEqual(context_form['group'].value(), post.group.id)

    def test_commenting_redirect_to_login_page_for_guest_user(self):
        response = self.guest_client.get(
            reverse(
                ADD_COMMENT_URL,
                kwargs={'post_id': PostsPagesTests.POST_ID}
            ),
            follow=True
        )
        self.assertTemplateUsed(response, 'users/login.html')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_author = User.objects.create_user(username=POST_AUTHOR_USERNAME)
        Group.objects.create(
            title='Тестовый заголовок',
            slug=GROUP_SLUG,
            description='Тестовое описание'
        )
        Post.objects.bulk_create([
            Post(
                text=f'{POST_TEXT} {i}',
                author=post_author,
                group=Group.objects.get(slug=GROUP_SLUG)
            ) for i in range(16)
        ])

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_first_page_contains_ten_records(self):
        response = self.authorized_client.get(INDEX_URL)
        self.assertEqual(
            len(response.context['page_obj']),
            settings.COUNT_PAGE_POSTS
        )

    def test_group_list_first_page_contains_ten_records(self):
        response = self.authorized_client.get(GROUP_LIST_URL)
        self.assertEqual(
            len(response.context['page_obj']),
            settings.COUNT_PAGE_POSTS
        )

    def test_profile_first_page_contains_ten_records(self):
        response = self.authorized_client.get(PROFILE_URL)
        self.assertEqual(
            len(response.context['page_obj']),
            settings.COUNT_PAGE_POSTS
        )
