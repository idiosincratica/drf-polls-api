from rest_framework import generics
from ..serializers.response import TextResponseSerializer, SingleChoiceResponseSerializer,\
    MultipleChoicesResponseSerializer
from ..mixins import AtomicCreateMixin


class CreateTextResponse(generics.CreateAPIView):
    serializer_class = TextResponseSerializer


class CreateSingleChoiceResponse(generics.CreateAPIView):
    serializer_class = SingleChoiceResponseSerializer


class CreateMultipleChoicesResponse(AtomicCreateMixin, generics.CreateAPIView):
    serializer_class = MultipleChoicesResponseSerializer
