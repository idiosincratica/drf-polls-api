from rest_framework import generics
from ..serializers.response import TextResponseSerializer, SingleChoiceResponseSerializer, MultipleChoicesResponseSerializer


class CreateTextResponse(generics.CreateAPIView):
    serializer_class = TextResponseSerializer


class CreateSingleChoiceResponse(generics.CreateAPIView):
    serializer_class = SingleChoiceResponseSerializer


class CreateMultipleChoicesResponse(generics.CreateAPIView):
    serializer_class = MultipleChoicesResponseSerializer
