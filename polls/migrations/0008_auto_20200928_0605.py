# Generated by Django 3.1.1 on 2020-09-28 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20200922_1830'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='multiplechoicesresponse',
            name='user_choice_constraint',
        ),
        migrations.RemoveConstraint(
            model_name='singlechoiceresponse',
            name='single_choice_responce_user_question_constraint',
        ),
        migrations.RemoveConstraint(
            model_name='singlechoiceresponse',
            name='single_choice_responce_user_choice_constraint',
        ),
        migrations.RemoveConstraint(
            model_name='textresponse',
            name='text_response_user_question_constraint',
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=30, verbose_name='Response text'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='end',
            field=models.DateField(verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start',
            field=models.DateField(verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=256, verbose_name='Question text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Text'), (2, 'Single choice'), (3, 'Multiple choices')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='textresponse',
            name='text',
            field=models.TextField(verbose_name='Response text'),
        ),
        migrations.AddConstraint(
            model_name='choice',
            constraint=models.UniqueConstraint(fields=('question', 'text'), name='choice__question_text__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='multiplechoicesresponse',
            constraint=models.UniqueConstraint(fields=('user', 'choice'), name='multiple_choices_responses__user__choice__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='singlechoiceresponse',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='single_choice_responce__user__question__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='singlechoiceresponse',
            constraint=models.UniqueConstraint(fields=('user', 'choice'), name='single_choice_responce__user__choice__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='textresponse',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='text_response__user__question__unique_constraint'),
        ),
    ]
