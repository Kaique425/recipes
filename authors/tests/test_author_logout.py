from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        response = self.client.get(reverse("author:logout"))
        status_code = response.status_code
        self.assertEqual(405, status_code)

    def test_user_tries_logout_being_logged_and_using_post_method(self):
        user = User.objects.create_user(
            username="TestUsername",
            password="TestPassword",
        )
        self.client.login(username="TestUsername", password="TestPassword")
        response = self.client.post(
            reverse("author:logout"),
            data={
                "username": "TestUsername",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)

    def test_if_user_tries_to_logout_another_user(self):
        User.objects.create_user(username="TestUsername", password="TestPassword")
        self.client.login(username="TestUsername", password="TestPassword")

        response = self.client.post(
            reverse("author:logout"),
            data={
                "username1": "TestUsername",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("Invalid user logout", response.content.decode("utf-8"))

    def test_user_tries_to_logout_without_being_logged(self):
        response = self.client.post(reverse("author:logout"), follow=False)
        status_code = response.status_code
        self.assertEqual(302, status_code)
