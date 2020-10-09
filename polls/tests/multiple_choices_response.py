from django.urls import reverse
from rest_framework.test import APITestCase
from anonymous_auth.models import User
from .init import populate_db, AuthenitcateAnonymousUserMixin


class MultipleChoicesResponseTests(AuthenitcateAnonymousUserMixin, APITestCase):
    def test_multi_not_exist(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choices": [90]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_ok(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_started(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "choices": [8]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_not_authenticated_user(self):
        populate_db()
        data = {
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'not_authenticated', status_code=401)

    def test_nonexistent_token(self):
        populate_db()
        user = User.objects.create()
        token = user.key
        user.delete()
        user = User.objects.create()
        assert(token != user.key)
        self.client.credentials(HTTP_AUTHORIZATION='Anonymous ' + token)
        data = {
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'authentication_failed', status_code=401)

    def test_empty_choices(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": []
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Choices list must not be empty', status_code=400)

    def test_inexistent_choices(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": [8465, 8825]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, f'Some choices don\'t exist: 8465, 8825', status_code=400)

    def test_singular_question(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": [5, 7]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, f'All choices must refer to one question. Referred questions: 5, 6', status_code=400)

    def test_question_already_set(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": [5]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        data = {
            "user": 1,
            "choices": [6]
        }
        response = self.client.post(url, data)
        self.assertContains(response, f'Some choices are already set for the referred question: 5', status_code=400)

    def test_question_type(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": [2]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'The referred question must be of type 3', status_code=400)

    def test_ended_poll(self):
        populate_db()
        self.authenticate_anonymous_user()
        data = {
            "user": 1,
            "choices": [9]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'The referred poll has expired', status_code=400)
