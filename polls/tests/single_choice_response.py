from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import User
from .init import populate_db


class SingleChoiceResponseTests(APITestCase):
    def test_ok(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_bad_user(self):
        populate_db()
        User().save()
        data = {
            "user": 100,
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'does not exist', status_code=400)

    def test_started(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choice": 10
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_duplicate(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_others_choice(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choice": 5
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_question_type(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choice": 5
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Choice must refer to a question of type 2', status_code=400)