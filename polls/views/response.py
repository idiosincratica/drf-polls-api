from rest_framework import generics
from ..serializers.response import TextResponseSerializer, SingleChoiceResponseSerializer,\
    MultipleChoicesResponseSerializer
from ..mixins import AtomicCreateMixin, CreateWithUserMixin
from anonymous_auth.permissions import IsAnonymousUserWithCredentials


class CreateTextResponse(CreateWithUserMixin, generics.CreateAPIView):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = TextResponseSerializer


class CreateSingleChoiceResponse(CreateWithUserMixin, generics.CreateAPIView):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = SingleChoiceResponseSerializer


class CreateMultipleChoicesResponse(AtomicCreateMixin, CreateWithUserMixin, generics.CreateAPIView):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = MultipleChoicesResponseSerializer
