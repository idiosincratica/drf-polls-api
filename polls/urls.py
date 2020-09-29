from django.urls import path
from django.http import JsonResponse
from rest_framework.authtoken import views
from .views import default, poll, question, choice, response, user

urlpatterns = [
    path('', default.default, name='default'),
    path('token', views.obtain_auth_token, name='token'),
    path('user', user.UserCreate.as_view(), name='user'),
    path('polls', poll.PollList.as_view(), name='polls'),
    path('active-polls', poll.PollActiveList.as_view(), name='active_polls'),
    path('poll', poll.PollCreate.as_view(), name='poll'),
    path('poll/<int:pk>', poll.PollRetrieveUpdateDestroy.as_view(), name='poll_pk'),
    path('question', question.QuestionCreate.as_view(), name='question'),
    path('question/<int:pk>', question.QuestionRetrieveUpdateDestroy.as_view(), name='question_pk'),
    path('choice', choice.ChoiceCreate.as_view(), name='choice'),
    path('choice/<int:pk>', choice.ChoiceRetrieveUpdateDestroy.as_view(), name='choice_pk'),
    path('text-response', response.CreateTextResponse.as_view(), name='text_response'),
    path('single-choice-response', response.CreateSingleChoiceResponse.as_view(), name='single_choice_response'),
    path('multiple-choices-response', response.CreateMultipleChoicesResponse.as_view(), name='multiple_choices_response'),
    path('finished-polls', poll.PollFinishedListView.as_view(), name='finished_polls'),
    path('unfinished-polls', poll.PollUnfinishedListView.as_view(), name='unfinished_polls')
]
