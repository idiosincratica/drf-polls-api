from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import User
from .init import populate_db


class MultipleChoicesResponseTests(APITestCase):
    def test_multi_not_exist(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [90]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_ok(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_started(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [8]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, "The referred poll has not started yet", status_code=400)

    def test_nonexistent_user(self):
        populate_db()
        User().save()
        data = {
            "user": 100,
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'User does not exist', status_code=400)

    def test_malformed_user(self):
        populate_db()
        User().save()
        data = {
            "user": "what?",
            "choices": [5, 6]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'A valid integer is required', status_code=400)

    def test_empty_choices(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": []
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'Choices list must not be empty', status_code=400)

    def test_inexistent_choices(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [8465, 8825]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, f'Some choices don\'t exist: 8465, 8825', status_code=400)

    def test_singular_question(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [5, 7]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, f'All choices must refer to one question. Referred questions: 5, 6', status_code=400)

    def test_duplication(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [5]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        data = {
            "user": 1,
            "choices": [5, 6]
        }
        response = self.client.post(url, data)
        self.assertContains(response, f'Some choices are already set: 5', status_code=400)

    def test_question_type(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [2]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'The referred question must be of type 3', status_code=400)

    def test_ended_poll(self):
        populate_db()
        User().save()
        data = {
            "user": 1,
            "choices": [9]
        }
        url = reverse('multiple_choices_response')
        response = self.client.post(url, data)
        self.assertContains(response, 'The referred poll has expired', status_code=400)
