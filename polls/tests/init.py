from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from datetime import timedelta
from ..models import Poll, Question, Choice


def create_admin():
    User = get_user_model()
    return User.objects.create_user('admin', 'admin@test.com', '1', is_staff=True)


def get_started_poll():
    today = localdate()
    start = today
    end = today + timedelta(days=10)
    data = {
        "id": 1,
        "name": "First poll",
        "start": today,
        "end": end,
        "description": "this is first poll"
    }
    return data


def get_pending_poll():
    today = localdate()
    start = today + timedelta(days=10)
    end = today + timedelta(days=20)
    data = {
        "id": 2,
        "name": "First poll",
        "start": start,
        "end": end,
        "description": "this is first poll"
    }
    return data


def get_ended_poll():
    today = localdate()
    start = today - timedelta(days=10)
    end = today
    data = {
        "id": 3,
        "name": "First poll",
        "start": start,
        "end": end,
        "description": "this is an ended poll"
    }
    return data


def populate_db():
    Poll(**get_started_poll()).save()
    Poll(**get_pending_poll()).save()
    Poll(**get_ended_poll()).save()

    question = {
        "id": 1,
        "poll_id": 1,
        "text": "started poll first text question",
        "type": 1
    }
    Question(**question).save()
    question = {
        "id": 2,
        "poll_id": 1,
        "text": "started poll second single choice question",
        "type": 2
    }
    Question(**question).save()
    question = {
        "id": 3,
        "poll_id": 2,
        "text": "pending poll first text question",
        "type": 1
    }
    Question(**question).save()
    question = {
        "id": 4,
        "poll_id": 2,
        "text": "pending poll second single choice question",
        "type": 2
    }
    Question(**question).save()
    question = {
        "id": 5,
        "poll_id": 1,
        "text": "started poll third multiple choices question",
        "type": 3
    }
    Question(**question).save()
    question = {
        "id": 6,
        "poll_id": 2,
        "text": "pending poll multiple choices question",
        "type": 3
    }
    Question(**question).save()
    question = {
        "id": 7,
        "poll_id": 3,
        "text": "ended poll multiple choices question",
        "type": 3
    }
    Question(**question).save()

    choice = {
        "id": 1,
        "question_id": 2,
        "text": "choice 1"
    }
    Choice(**choice).save()
    choice = {
        "id": 2,
        "question_id": 2,
        "text": "choice 2"
    }
    Choice(**choice).save()
    choice = {
        "id": 3,
        "question_id": 4,
        "text": "choice 2"
    }
    Choice(**choice).save()
    choice = {
        "id": 4,
        "question_id": 5,
        "text": "multi choice 1"
    }
    Choice(**choice).save()
    choice = {
        "id": 5,
        "question_id": 5,
        "text": "multi choice 2"
    }
    Choice(**choice).save()
    choice = {
        "id": 6,
        "question_id": 5,
        "text": "multi choice 3"
    }
    Choice(**choice).save()
    choice = {
        "id": 7,
        "question_id": 6,
        "text": "multi choice 1"
    }
    Choice(**choice).save()
    choice = {
        "id": 8,
        "question_id": 6,
        "text": "multi choice 2"
    }
    Choice(**choice).save()
    choice = {
        "id": 9,
        "question_id": 7,
        "text": "multi choice 1"
    }
    Choice(**choice).save()
    choice = {
        "id": 10,
        "question_id": 4,
        "text": "choice 1"
    }
    Choice(**choice).save()


