from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import User
from .init import populate_db


class TextResponseTests(APITestCase):
    def test_ok(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "question": 1,
            "text": "hello"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_nonexistent_user(self):
        populate_db()
        User().save()
        data = {
            "user": 100,
            "question": 1,
            "text": "i'm here"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'does not exist', status_code=400)

    def test_malformed_user(self):
        populate_db()
        User().save()
        data = {
            "user": "joke",
            "question": 1,
            "text": "i'm here"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Incorrect type. Expected pk value, received str', status_code=400)

    def test_started(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "question": 3,
            "text": "hehe"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_duplicate(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "question": 1,
            "text": "that's it"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_question_type(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "question": 2,
            "text": "some text"
        }
        url = reverse('text_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Question must be of type 1', status_code=400)