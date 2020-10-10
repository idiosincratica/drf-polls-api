from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .init import populate_db, create_admin


class ChoiceTests(APITestCase):
    def auth_admin(self):
        self.client.force_authenticate(user=create_admin())

    def test_delete_started(self):
        populate_db()
        self.auth_admin()
        response = self.client.delete(reverse('choice-detail', args=[1]))
        self.assertContains(response, 'Deleting choices referring to started polls is forbidden', status_code=400)

    def test_delete_ok(self):
        populate_db()
        self.auth_admin()
        response = self.client.delete(reverse('choice-detail', args=[7]))
        self.assertEqual(response.status_code, 204)

    def test_create_ok(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-list')
        data = {
            "question": 4,
            "text": "something here"
        }
        response = self.client.post(url, data)
        data['text'] += 'x'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-list')
        data = {
            "question": 2,
            "text": "so"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-detail', args=[4])
        data = {
            "text": "sojsjhasdf"
        }
        response = self.client.patch(url, data)
        self.assertContains(response, 'Modification of choices belonging to started polls is forbidden',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_update_pending_to_started(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-detail', args=[6])
        data = {
            "question": 5
        }
        response = self.client.patch(url, data)
        self.assertContains(response, "Can't add choices to questions referring to a started poll",
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-list')
        data = {
            "question": 4,
            "text": "so"
        }
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertContains(response, 'The fields question, text must make a unique set',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_update_duplicate(self):
        populate_db()
        self.auth_admin()
        url = reverse('choice-list')
        data = {
            "question": 6,
            "text": "multi choice 1"
        }
        response = self.client.post(url, data)
        self.assertContains(response, 'The fields question, text must make a unique set',
                            status_code=status.HTTP_400_BAD_REQUEST)