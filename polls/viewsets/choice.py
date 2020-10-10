from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAdminUser
from ..serializers.choice import ChoiceSerializer
from ..models import Choice
from ..mixins import AtomicCreateMixin, AtomicUpdateMixin, DestroyStartedMixin


class ChoiceViewSet(DestroyStartedMixin, AtomicUpdateMixin, AtomicCreateMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    destroy_started = ('question.poll', 'Deleting choices referring to started polls is forbidden')