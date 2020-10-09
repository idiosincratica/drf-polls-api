from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.utils.timezone import localdate
from django.db.models import Q, OuterRef, Exists
from ..serializers.poll import PollSerializer, PollListSerializer, PollFinishedListSerializer
from ..models import Poll, Question
from anonymous_auth.models import User
from ..permissions import IsAdminUserOrReadOnly
from anonymous_auth.permissions import IsAnonymousUserWithCredentials
from ..mixins import AtomicUpdateMixin


class PollList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollActiveList(generics.ListAPIView):
    serializer_class = PollListSerializer

    def get_queryset(self):
        today = localdate()
        return Poll.objects.filter(start__lte=today, end__gt=today)


class PollCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PollSerializer


class PollRetrieveUpdateDestroy(AtomicUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class BasePollRespondedListView(generics.ListAPIView):
    """
    Collect data for construction of querysets that provide finish and unfinished polls
    """
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = PollFinishedListSerializer

    def get_user_polls_query(self, user):
        """
        Select all the polls that have been responded by the user, completely or partially
        """
        return Poll.objects.filter(Q(questions__text_responses__user=user)
                                   | Q(questions__choices__single_choice_responses__user=user)
                                   | Q(questions__choices__multiple_choices_responses__user=user))

    def get_no_response_subquery(self, user):
        """
        Select all the questions with no response
        """
        return Question.objects.filter(poll=OuterRef('pk')).exclude(Q(choices__single_choice_responses__user=user)
                                       | Q(choices__multiple_choices_responses__user=user)
                                             | Q(text_responses__user=user))

    def get_query_elements(self):
        user = self.request.auth

        return {
            'user': user,
            'user_polls_query': self.get_user_polls_query(user),
            'no_response_subquery': self.get_no_response_subquery(user)
        }


class PollFinishedListView(BasePollRespondedListView):
    """
    Polls with every question being responded by the user
    """

    def get_queryset(self):
        elements = self.get_query_elements()

        # exclude polls that have questions with no response
        return elements['user_polls_query'].exclude(Exists(elements['no_response_subquery'])).distinct()


class PollUnfinishedListView(PollFinishedListView):
    """
    Polls that have some questions not responded by the user
    """

    def get_queryset(self):
        elements = self.get_query_elements()

        # Keep only the polls having questions not responded by the user
        return elements['user_polls_query'].filter(Exists(elements['no_response_subquery'])).distinct()

