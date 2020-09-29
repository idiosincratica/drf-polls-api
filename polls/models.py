from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def format_str(id, text):
    return f'#{id} {text}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(models.Model):
    pass


class Poll(models.Model):
    name = models.CharField('Name', max_length=20)
    start = models.DateField('Start date')
    end = models.DateField('End date')
    description = models.TextField('Description')

    def __str__(self):
        return format_str(self.pk, self.name)


class Question(models.Model):
    types = {
        1: 'Text',
        2: 'Single choice',
        3: 'Multiple choices'
    }
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField('Question text', max_length=256)
    type = models.PositiveSmallIntegerField('Type', choices=list(types.items()))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['poll', 'text'], name='question__poll__text__unique_constraint')
        ]

    def __str__(self):
        return format_str(self.pk, self.text)


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField('Response text', max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'text'], name='choice__question__text__unique_constraint')
        ]

    def __str__(self):
        return format_str(self.pk, self.text)


class TextResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='text_responses', on_delete=models.CASCADE)
    text = models.TextField('Response text')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'],
                                    name='text_response__user__question__unique_constraint')
        ]

    def __str__(self):
        return format_str(self.pk, self.text)


class SingleChoiceResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='single_choice_responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # enforce data consistency

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'],
                                    name='single_choice_response__user__question__unique_constraint'),
            models.UniqueConstraint(fields=['user', 'choice'],
                                    name='single_choice_response__user__choice__unique_constraint')
        ]

    def save(self, *args, **kwargs):
        self.question = self.choice.question
        super().save(*args, **kwargs)


class MultipleChoicesResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='multiple_choices_responses', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'choice'],
                                    name='multiple_choices_responses__user__choice__unique_constraint')
        ]
