from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from anonymous_auth.views import ObtainAnonymousToken
from polls import viewsets

router = DefaultRouter(trailing_slash=False)

router.register('polls', viewsets.PollListViewSet, basename='polls')
router.register('active-polls', viewsets.PollActiveListViewSet, basename='active_polls')
router.register('poll', viewsets.PollViewSet, basename='poll')
router.register('question', viewsets.QuestionViewSet, basename='question')
router.register('choice', viewsets.ChoiceViewSet, basename='choice')
router.register('text-response', viewsets.TextResponseViewSet, basename='text_response')
router.register('single-choice-response', viewsets.SingleChoiceResponseViewSet, basename='single_choice_response')
router.register('multiple-choices-response', viewsets.MultipleChoicesResponseViewSet,
                basename='multiple_choices_response')
router.register('finished-polls', viewsets.PollFinishedListViewSet, basename='finished_polls')
router.register('unfinished-polls', viewsets.PollUnfinishedListViewSet, basename='unfinished_polls')

urlpatterns = [
    path('token', views.obtain_auth_token, name='token'),
    path('anonymous-token', ObtainAnonymousToken.as_view(), name='anonymous_token'),
    path('', include(router.urls))
]
