from django.urls import reverse
from django.utils.timezone import localdate
from rest_framework.test import APITestCase
from datetime import timedelta
from ..models import Poll, User, TextResponse, SingleChoiceResponse, MultipleChoicesResponse
from .init import create_admin, populate_db, get_started_poll, get_pending_poll

def populate_db_one_finished_poll():
    User().save()
    MultipleChoicesResponse(**{
        "user_id": 1,
        "choice_id": 9
    }).save()

def populate_db_two_finished_polls():
    User().save()
    MultipleChoicesResponse(**{
        "user_id": 1,
        "choice_id": 9
    }).save()
    MultipleChoicesResponse(**{
        "user_id": 1,
        "choice_id": 7
    }).save()
    SingleChoiceResponse(**{
        "user_id": 1,
        "choice_id": 10
    }).save()
    TextResponse(**{
        "user_id": 1,
        "question_id": 3,
        "text": "helklkh"
    }).save()

def populate_db_one_finished_one_unfinished_poll():
    User().save()
    MultipleChoicesResponse(**{
        "user_id": 1,
        "choice_id": 9
    }).save()
    MultipleChoicesResponse(**{
        "user_id": 1,
        "choice_id": 7
    }).save()
    # MultipleChoicesResponse(**{
    #     "user_id": 1,
    #     "choice_id": 8
    # }).save()
    TextResponse(**{
        "user_id": 1,
        "question_id": 3,
        "text": "helklkh"
    }).save()


class PollsTests(APITestCase):
    def setUp(self):
        self.admin = create_admin()

    def test_active_polls_empty(self):
        url = reverse('active_polls')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_active_polls_exist(self):
        data = {
            "name": "Some poll",
            "start": "2020-09-01",
            "end": "2020-10-03",
            "description": "jj"
        }
        Poll(**data).save()
        url = reverse('active_polls')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{
            "id": 1,
            "name": "Some poll",
            "start": "2020-09-01",
            "end": "2020-10-03",
            "description": "jj"
        }])

    def test_put_started(self):
        populate_db()
        self.client.force_authenticate(user=self.admin)
        poll = get_started_poll()
        poll['description'] = 'changed'
        poll['start'] = localdate() + timedelta(days=1)
        url = reverse('poll_pk', args=[1])
        response = self.client.put(url, poll)
        self.assertEqual(response.status_code, 400)

    def test_finished_with_one_finished(self):
        populate_db()
        populate_db_one_finished_poll()
        url = reverse('finished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_with_two_finished(self):
        populate_db()
        populate_db_two_finished_polls()
        url = reverse('finished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_finished_with_one_finished_one_unfinished(self):
        populate_db()
        populate_db_one_finished_one_unfinished_poll()
        url = reverse('finished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_with_nothing_finished(self):
        populate_db()
        User().save()
        url = reverse('finished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_nothing_finished(self):
        populate_db()
        User().save()
        url = reverse('unfinished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_one_finished(self):
        populate_db()
        User().save()
        populate_db_one_finished_poll()
        url = reverse('unfinished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_two_finished(self):
        populate_db()
        User().save()
        populate_db_two_finished_polls()
        url = reverse('unfinished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_one_finished_one_unfinished(self):
        populate_db()
        populate_db_one_finished_one_unfinished_poll()
        url = reverse('unfinished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_user_does_not_exist(self):
        populate_db()
        url = reverse('finished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertContains(response, 'does not exist', status_code=400)

    def test_unfinished_user_does_not_exist(self):
        populate_db()
        url = reverse('unfinished_polls')
        response = self.client.get(url, data={'user': 1})
        self.assertContains(response, 'does not exist', status_code=400)