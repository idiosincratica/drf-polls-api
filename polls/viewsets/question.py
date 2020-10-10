from rest_framework.viewsets import GenericViewSet, mixins
from ..serializers.question import QuestionSerializer
from ..models import Question
from ..permissions import IsAdminUserOrReadOnly
from ..mixins import AtomicUpdateMixin, AtomicCreateMixin, DestroyStartedMixin


class QuestionViewSet(DestroyStartedMixin, AtomicUpdateMixin, AtomicCreateMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    destroy_started = ('poll', 'Deleting questions referring to started polls is forbidden')
