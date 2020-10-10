from rest_framework.viewsets import GenericViewSet, mixins
from ..serializers.response import TextResponseSerializer, SingleChoiceResponseSerializer,\
    MultipleChoicesResponseSerializer
from ..mixins import AtomicCreateMixin, CreateWithUserMixin
from anonymous_auth.permissions import IsAnonymousUserWithCredentials


class TextResponseViewSet(CreateWithUserMixin, mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = TextResponseSerializer


class SingleChoiceResponseViewSet(CreateWithUserMixin, mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = SingleChoiceResponseSerializer


class MultipleChoicesResponseViewSet(AtomicCreateMixin, CreateWithUserMixin, mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [IsAnonymousUserWithCredentials]
    serializer_class = MultipleChoicesResponseSerializer
