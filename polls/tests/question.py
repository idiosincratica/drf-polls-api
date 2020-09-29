from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .init import populate_db, create_admin


class QuestionTests(APITestCase):
    def setUp(self):
        pass

    def auth_admin(self):
        self.client.force_authenticate(user=create_admin())

    def test_delete_started(self):
        populate_db()
        self.auth_admin()
        response = self.client.delete(reverse('question_pk', args=[1]))
        self.assertContains(response, 'Deleting questions referring to started polls is forbidden', status_code=400)

    def test_delete_ok(self):
        populate_db()
        self.auth_admin()
        response = self.client.delete(reverse('question_pk', args=[3]))
        self.assertEqual(response.status_code, 204)

    def test_create_ok(self):
        populate_db()
        self.auth_admin()
        url = reverse('question')
        data = {
            "poll": 2,
            "text": "something here",
            "type": 1
        }
        response = self.client.post(url, data)
        data['text'] += 'x'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('question')
        data = {
            "poll": 1,
            "text": "so",
            "type": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('question_pk', args=[5])
        data = {
            "text": "sjfdo",
            "type": 1
        }
        response = self.client.patch(url, data)
        self.assertContains(response, 'Modification of questions belonging to started polls is forbidden',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_update_to_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('question_pk', args=[6])
        data = {
            "poll": 1
        }
        response = self.client.patch(url, data)
        self.assertContains(response, 'Adding questions to started polls is forbidden',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate(self):
        populate_db()
        self.auth_admin()
        url = reverse('question')
        data = {
            "poll": 2,
            "text": "so",
            "type": 1
        }
        response = self.client.post(url, data)
        data['type'] = 2
        response = self.client.post(url, data)
        self.assertContains(response, 'The fields poll, text must make a unique set',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_update_duplicate(self):
        populate_db()
        self.auth_admin()
        url = reverse('question')
        data = {
            "poll": 2,
            "text": "pending poll multiple choices question",
            "type": 1
        }
        response = self.client.post(url, data)
        self.assertContains(response, 'The fields poll, text must make a unique set',
                            status_code=status.HTTP_400_BAD_REQUEST)