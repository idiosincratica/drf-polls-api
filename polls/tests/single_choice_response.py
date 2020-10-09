from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from anonymous_auth.models import User
from .init import populate_db, AuthenitcateAnonymousUserMixin


class SingleChoiceResponseTests(AuthenitcateAnonymousUserMixin, APITestCase):
    def test_ok(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_not_authenticated(self):
        populate_db()
        data = {
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'not_authenticated', status_code=status.HTTP_401_UNAUTHORIZED)

    def test_started(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choice": 10
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_duplicate(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choice": 1
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_others_choice(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choice": 5
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_question_type(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choice": 5
        }
        url = reverse('single_choice_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Choice must refer to a question of type 2', status_code=400)