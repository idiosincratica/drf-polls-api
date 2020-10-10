from django.urls import reverse
from rest_framework.test import APITestCase
from django.utils.timezone import localdate
from datetime import timedelta
from ..models import Poll, TextResponse, SingleChoiceResponse, MultipleChoicesResponse
from anonymous_auth.models import User
from .init import create_admin, populate_db, get_started_poll, AuthenitcateAnonymousUserMixin

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


class PollsTests(AuthenitcateAnonymousUserMixin, APITestCase):
    def setUp(self):
        self.admin = create_admin()

    def authenticate_first_user(self):
        user = User.objects.get(pk=1)
        self.client.credentials(HTTP_AUTHORIZATION='Anonymous ' + user.key)

    def test_active_polls_empty(self):
        url = reverse('active_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_active_polls_exist(self):
        today = localdate()
        start = str(today - timedelta(days=5))
        end = str(today + timedelta(days=10))
        data = {
            "name": "Some poll",
            "start": start,
            "end": end,
            "description": "jj"
        }
        Poll(**data).save()
        url = reverse('active_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{
            "id": 1,
            "name": "Some poll",
            "start": start,
            "end": end,
            "description": "jj"
        }])

    def test_put_started(self):
        populate_db()
        self.client.force_authenticate(user=self.admin)
        poll = get_started_poll()
        poll['description'] = 'changed'
        poll['start'] = localdate() + timedelta(days=1)
        url = reverse('poll-detail', args=[1])
        response = self.client.put(url, poll)
        self.assertEqual(response.status_code, 400)

    def test_finished_with_one_finished(self):
        populate_db()
        populate_db_one_finished_poll()
        url = reverse('finished_polls-list')
        self.authenticate_first_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_with_two_finished(self):
        populate_db()
        populate_db_two_finished_polls()
        self.authenticate_first_user()
        url = reverse('finished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_finished_with_one_finished_one_unfinished(self):
        populate_db()
        populate_db_one_finished_one_unfinished_poll()
        self.authenticate_first_user()
        url = reverse('finished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_with_nothing_finished(self):
        populate_db()
        User().save()
        self.authenticate_anonymous_user()
        url = reverse('finished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_nothing_finished(self):
        populate_db()
        User().save()
        self.authenticate_anonymous_user()
        url = reverse('unfinished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_one_finished(self):
        populate_db()
        User().save()
        self.authenticate_anonymous_user()
        populate_db_one_finished_poll()
        url = reverse('unfinished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_two_finished(self):
        populate_db()
        User().save()
        self.authenticate_anonymous_user()
        populate_db_two_finished_polls()
        url = reverse('unfinished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unfinished_with_one_finished_one_unfinished(self):
        populate_db()
        populate_db_one_finished_one_unfinished_poll()
        self.authenticate_first_user()
        url = reverse('unfinished_polls-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_finished_not_authenticated(self):
        populate_db()
        url = reverse('finished_polls-list')
        response = self.client.get(url, data={'user': 1})
        self.assertContains(response, 'not_authenticated', status_code=401)

    def test_unfinished_not_authenticated(self):
        populate_db()
        url = reverse('unfinished_polls-list')
        response = self.client.get(url, data={'user': 1})
        self.assertContains(response, 'not_authenticated', status_code=401)