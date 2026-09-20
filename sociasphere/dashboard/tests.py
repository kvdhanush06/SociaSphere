from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import ProfilePicForm
from .models import Post, Profile


class MutationSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='StrongTestPassword123!',
        )
        self.other_user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='StrongTestPassword123!',
        )
        self.post = Post.objects.create(user=self.user, body='private post')

    def test_state_changing_endpoints_reject_get(self):
        for name, args in (
            ('logout', None),
            ('post_like', [self.post.pk]),
            ('follow', [self.other_user.pk]),
            ('unfollow', [self.other_user.pk]),
            ('delete_post', [self.post.pk]),
        ):
            self.client.force_login(self.user)
            url = reverse(name, args=args) if args else reverse(name)
            self.assertEqual(self.client.get(url, secure=True).status_code, 405, name)

    def test_delete_post_requires_ownership(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse('delete_post', args=[self.post.pk]), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_like_requires_authentication(self):
        response = self.client.post(reverse('post_like', args=[self.post.pk]), secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.post.likes.filter(pk=self.user.pk).exists())

    def test_profile_url_form_rejects_javascript_scheme(self):
        profile = Profile.objects.get(user=self.user)
        form = ProfilePicForm(
            data={
                'profile_bio': '',
                'homepage_link': 'javascript:alert(1)',
                'facebook_link': '',
                'instagram_link': '',
                'linkedin_link': '',
            },
            instance=profile,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('homepage_link', form.errors)
