from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from ..serializers.choice import ChoiceSerializer
from ..models import Choice
from ..mixins import AtomicCreateMixin, AtomicUpdateMixin, DestroyStartedMixin


class ChoiceCreate(AtomicCreateMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChoiceSerializer


class ChoiceRetrieveUpdateDestroy(DestroyStartedMixin, AtomicUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    destroy_started = (lambda instance: instance.question.poll,
                       'Deleting choices referring to started polls is forbidden')
