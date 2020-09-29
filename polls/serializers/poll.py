from rest_framework import serializers
from django.utils.timezone import localdate
from ..models import Poll
from ..helpers import poll_started, validate_poll_active
from ..mixins import IsAdminMixin
from .question import QuestionFinishedSerializer
from polls import error_codes


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start', 'end']


class PollSerializer(serializers.ModelSerializer, IsAdminMixin):
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'start', 'end', 'description', 'questions']

    def to_representation(self, instance):
        """deny access for anonymous users to the polls with inappropriate date range"""
        if not self.is_admin():
            validate_poll_active(instance)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        if poll_started(self.instance):
            raise serializers.ValidationError("Modification of a started poll is forbidden", error_codes.POLL_STARTED)
        if 'start' in validated_data and validated_data['start'] != self.instance.start:
            raise serializers.ValidationError(
                {'start': f'Start date should not be modified. Current value is "{self.instance.start}"'},
                error_codes.POLL_START_DATE_MODIFIED)
        return super().update(instance, validated_data)

    def validate_start(self, start):
        if start <= localdate():
            raise serializers.ValidationError("Start date must be set in the future",
                                              error_codes.POLL_START_DATE_NOT_IN_FUTURE)
        else:
            return start

    def validate(self, data):
        start = data['start'] if 'start' in data else self.instance.start
        end = data['end'] if 'end' in data else self.instance.end
        if end <= start:
            raise serializers.ValidationError({"end": "End date must be greater than start date"},
                                              error_codes.POLL_END_NOT_GREATER_THAN_START)
        return data


class PollFinishedListSerializer(serializers.ModelSerializer):
    questions = QuestionFinishedSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'start', 'end', 'description', 'questions']