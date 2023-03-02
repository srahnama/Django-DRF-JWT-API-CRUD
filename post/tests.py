from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post, Like, Unlike
from .serializers import PostSerializer, LikeSerializer, UnlikeSerializer

User = get_user_model()


class PostTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.post_data = {'title': 'Test Post', 'body': 'Test Content'}

    def test_post_create(self):
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_list(self):
        Post.objects.create(title='Post 1', body='Content 1', user=self.user)
        Post.objects.create(title='Post 2', body='Content 2', user=self.user)

        response = self.client.get('/api/posts/')

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        post = Post.objects.create(title='Test Post', body='Test Content', user=self.user)

        response = self.client.get(f'/api/posts/{post.id}/')

        serializer = PostSerializer(post)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update(self):
        post = Post.objects.create(title='Test Post', body='Test Content', user=self.user)
        updated_data = {'title': 'New Title', 'content': 'New Content'}

        response = self.client.put(f'/api/posts/{post.id}/', updated_data)

        post.refresh_from_db()

        self.assertEqual(post.title, 'New Title')
        self.assertEqual(post.body, 'New Content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        post = Post.objects.create(title='Test Post', body='Test Content', user=self.user)

        response = self.client.delete(f'/api/posts/{post.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LikeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', body='Test Content', user=self.user)

    def test_like_create(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/')

        like = Like.objects.first()
        serializer = LikeSerializer(like)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_delete(self):
        like = Like.objects.create(post=self.post, user=self.user)

        response = self.client.delete(f'/api/posts/{self.post.id}/like/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
