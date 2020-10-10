from django.urls import reverse
from rest_framework.test import APITestCase
from anonymous_auth.models import User
from .init import populate_db, AuthenitcateAnonymousUserMixin


class TextResponseTests(AuthenitcateAnonymousUserMixin, APITestCase):
    def test_ok(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "question": 1,
            "text": "hello"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_not_authenticated_anonymous(self):
        populate_db()
        data = {
            "question": 1,
            "text": "i'm here"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        self.assertContains(response, 'not_authenticated', status_code=401)

    def test_malformed_token(self):
        populate_db()
        user = User.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION='Anonymous ' + user.key[3:])
        data = {
            "question": 1,
            "text": "i'm here"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        self.assertContains(response, 'authentication_failed', status_code=401)

    def test_started(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "question": 3,
            "text": "hehe"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_duplicate(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "question": 1,
            "text": "that's it"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_question_type(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "question": 2,
            "text": "some text"
        }
        url = reverse('text_response-list')
        response = self.client.post(url, data)
        self.assertContains(response, 'Question must be of type 1', status_code=400)