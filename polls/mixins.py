from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .helpers import poll_started
from django.db import transaction



class IsAdminMixin:
    def is_admin(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user.is_staff
        else:
            return False


class RequestParamObjectMixin:
    def get_object_from_param(self, param_name, model):
        """retrieves an object from url query param"""
        id = self.request.query_params.get(param_name, None)

        if id is None:
            raise ParseError(f"{param_name} param must be provided")

        try:
            id = int(id)
        except (ValueError, TypeError):
            raise ParseError(f"Incorrect {param_name} param")

        try:
            return model.objects.get(pk=id)
        except model.DoesNotExist:
            raise ParseError(f'"{param_name}" does not exist')


class AtomicCreateMixin:
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicUpdateMixin:
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class DestroyStartedMixin:
    destroy_started = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if poll_started(self.destroy_started[0](instance)):
            raise ParseError(self.destroy_started[1])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)