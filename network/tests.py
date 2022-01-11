import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.user1 = get_user_model().objects.create(username="ahmed", email="a@a.com")
        self.user1.set_password("123")
        self.user1.is_active = True
        self.user1.save()
        self.profile_url = reverse("profile", args=[self.user1.username])
        self.following_url = reverse("following", args=[self.user1.username])
        self.post_url = reverse("post")
        self.login_url = reverse("login")

    def test_get_index(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/index.html")

    def test_create_user(self):
        self.user2 = get_user_model().objects.create(
            username="mahdy", email="m@m.com", password="123"
        )
        self.assertIs(self.user2.username, "mahdy")

    def test_profile_with_param(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)

    def test_following_with_param(self):
        response = self.client.get(self.following_url)

        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        login = self.client.post(
            self.login_url,
            {
                "username": self.user1.username,
                "email": self.user1.email,
                "password": "123",
            },
        )
        self.assertEqual(login.status_code, 200)
        
        response = self.client.post(self.post_url, json.dumps({"content": "new test post"}), 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(json.loads(response.content.decode("utf-8"))["data"]["pk"], 0)

    def test_post_update(self):
        login = self.client.post(
            self.login_url,
            {
                "username": self.user1.username,
                "email": self.user1.email,
                "password": "123",
            },
        )

        self.assertRedirects(login, self.index_url, 200)

        created = self.client.post(self.post_url, json.dumps({"content": "new test2 post"}), "application/json")
        self.assertEqual(created.status_code, 200)

        response = self.client.post(self.post_url, json.dumps({"pk": json.loads(created.content.decode("utf-8"))["data"]["pk"], "content": "new updated test2 post"}), "application/json")
        self.assertEqual(response.status_code, 204)
