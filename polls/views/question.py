from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from ..serializers.question import QuestionSerializer
from ..models import Question
from ..permissions import IsAdminUserOrReadOnly
from ..mixins import AtomicUpdateMixin, AtomicCreateMixin, DestroyStartedMixin


class QuestionCreate(AtomicCreateMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroy(DestroyStartedMixin, AtomicUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    destroy_started = ('poll', 'Deleting questions referring to started polls is forbidden')
