from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ..models import Question, TextResponse, Choice
from ..helpers import poll_started, validate_referred_poll_active
from ..mixins import IsAdminMixin
from polls import error_codes


class QuestionSerializer(serializers.ModelSerializer, IsAdminMixin):
    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'type']
        validators = [
            UniqueTogetherValidator(
                queryset=Question.objects.all(),
                fields=['poll', 'text']
            )
        ]

    def update(self, instance, validated_data):
        if poll_started(instance.poll):
            raise serializers.ValidationError("Modification of questions belonging to started polls is forbidden",
                                              error_codes.POLL_STARTED)
        """deletes related choices if setting question type to text"""
        if 'type' in validated_data and instance.type != validated_data['type'] and validated_data['type'] == 1:
            instance.choices.all().delete()
        return super().update(instance, validated_data)

    def validate_poll(self, poll):
        if poll_started(poll):
            raise serializers.ValidationError("Adding questions to started polls is forbidden",
                                              error_codes.CHANGE_TO_STARTED_POLL)
        return poll

    def to_representation(self, instance):
        if not self.is_admin():
            validate_referred_poll_active(instance.poll)

        result = super().to_representation(instance)
        if instance.type in (2, 3):
            result['choices'] = Choice.objects.filter(question=instance).values('id', 'text')
        return result


class QuestionFinishedSerializer(serializers.ModelSerializer):
    """Nested serializer for PollFinishedListSerializer"""

    response = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'response']

    def get_response(self, question):
        user = self.context['request'].query_params.get('user', None)
        if question.type == 1:
            obj = TextResponse.objects.filter(question=question, user=user).first()
            if obj is None:
                return None
            return obj.text
        elif question.type == 2:
            obj = Choice.objects.filter(question=question, single_choice_responses__user=user).first()
            if obj is None:
                return None
            return obj.text
        elif question.type == 3:
            objects = Choice.objects.filter(question=question, multiple_choices_responses__user=user).all()
            if len(objects) == 0:
                return None
            return [object.text for object in objects]
