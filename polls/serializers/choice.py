from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ..models import Choice, Question
from ..helpers import poll_started
from polls import error_codes


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text']

        validators = [
            UniqueTogetherValidator(
                queryset=Choice.objects.all(),
                fields=['question', 'text']
            )
        ]

    def update(self, instance, validated_data):
        if poll_started(instance.question.poll):
            raise serializers.ValidationError("Modification of choices belonging to started polls is forbidden",
                                              error_codes.POLL_STARTED)

        return super().update(instance, validated_data)

    def validate_question(self, question):
        if question.type not in (Question.Types.SINGLE_CHOICE, Question.Types.MULTIPLE_CHOICES):
            raise serializers.ValidationError("Can't add choice to question of type text",
                                              error_codes.WRONG_QUESTION_TYPE)

        if poll_started(question.poll):
            raise serializers.ValidationError("Can't add choices to questions referring to a started poll",
                                              error_codes.CHANGE_TO_STARTED_POLL)

        return question
