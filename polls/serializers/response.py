from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueTogetherValidator
from django.db.utils import IntegrityError
from ..models import TextResponse, SingleChoiceResponse, MultipleChoicesResponse, Choice, User, Question
from ..helpers import validate_referred_poll_active, render_list
from polls import error_codes


class TextResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextResponse
        fields = ['user', 'question', 'text']

        validators = [
            UniqueTogetherValidator(
                queryset=TextResponse.objects.all(),
                fields=['user', 'question']
            )
        ]

    def validate_question_type(self, question):
        if question.type != Question.Types.TEXT:
            raise serializers.ValidationError({'question': 'Question must be of type 1'},
                                              error_codes.WRONG_QUESTION_TYPE)

    def validate(self, data):
        validate_referred_poll_active(data['question'].poll)
        self.validate_question_type(data['question'])
        return data


class SingleChoiceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChoiceResponse
        fields = ['user', 'choice']

        validators = [
            UniqueTogetherValidator(
                queryset=SingleChoiceResponse.objects.all(),
                fields=['user', 'choice']
            )
        ]

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['question'] = data['choice'].question
        return data

    def validate_single_choice_per_question(self, user, question):
        response = SingleChoiceResponse.objects.filter(user=user, question=question).first()

        if response is not None:
            raise serializers.ValidationError('The referred question can have only one response',
                                              error_codes.QUESTION_MULTIPLE_RESPONSES)

    def validate_question_type(self, question):
        if question.type != Question.Types.SINGLE_CHOICE:
            raise serializers.ValidationError({'choice': 'Choice must refer to a question of type 2'},
                                              error_codes.WRONG_QUESTION_TYPE)

    def validate(self, data):
        validate_referred_poll_active(data['question'].poll)
        self.validate_single_choice_per_question(data['user'], data['question'])
        self.validate_question_type(data['question'])

        return data


class MultipleChoicesResponseSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    choices = serializers.ListField(child=serializers.IntegerField())

    def create_user(self, user):
        try:
            user = User.objects.get(pk=user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "User does not exist"}, error_codes.USER_DOES_NOT_EXIST)

        return user

    def create_choices(self, choices):
        choice_objects = Choice.objects.filter(pk__in=choices)
        return choice_objects

    def validate_empty_choices(self, choices):
        if len(choices) == 0:
            raise serializers.ValidationError({"choices": "Choices list must not be empty"},
                                              error_codes.CHOICES_LIST_EMPTY)

    def validate_choices_existence(self, choices, choice_objects):
        if len(choices) != len(choice_objects):
            choices_set = set(choices)
            choice_objects_set = {choice.pk for choice in choice_objects}
            bad_choices = choices_set - choice_objects_set
            raise serializers.ValidationError({'choices': f'Some choices don\'t exist: {render_list(bad_choices)}'},
                                              error_codes.CHOICE_DOES_NOT_EXIST)

    def validate_singular_question(self, choice_objects):
        questions = {choice.question_id for choice in choice_objects}

        if len(questions) > 1:
            raise serializers.ValidationError(
                {'choices': f'All choices must refer to one question. Referred questions: {render_list(questions)}'},
                error_codes.MULTIPLE_QUESTIONS_REFERRED)

    def validate_question_responded(self, user, question):
        responses = MultipleChoicesResponse.objects.filter(user=user, choice__question=question)

        if len(responses) > 0:
            choice_ids = [response.choice_id for response in responses]
            raise serializers.ValidationError(
                {'choices': f'Some choices are already set for the referred question: {render_list(choice_ids)}'},
                                              error_codes.QUESTION_ALREADY_RESPONDED)

    def validate_question_type(self, question):
        if question.type != Question.Types.MULTIPLE_CHOICES:
            raise serializers.ValidationError({'choices': 'The referred question must be of type 3'},
                                              error_codes.WRONG_QUESTION_TYPE)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        user = self.create_user(data['user'])
        choices = data['choices']

        self.validate_empty_choices(choices)
        choice_objects = self.create_choices(choices)
        self.validate_choices_existence(choices, choice_objects)

        return {
            'user': user,
            'choices': choice_objects
        }

    def validate(self, data):
        choices = data['choices']
        self.validate_singular_question(choices)
        question = choices[0].question
        validate_referred_poll_active(question.poll)
        self.validate_question_type(question)
        self.validate_question_responded(data['user'], question)

        return data

    def create(self, validated_data):
        user = validated_data['user']
        responses = [MultipleChoicesResponse(user=user, choice=choice) for choice in validated_data['choices']]
        saved = []

        try:
            for response in responses:
                response.save()
                saved.append(response.choice_id)
        except IntegrityError:
            raise APIException('Integrity error', error_codes.DB_INTEGRITY_ERROR)

        return {"user": user.id, "choices": saved}
