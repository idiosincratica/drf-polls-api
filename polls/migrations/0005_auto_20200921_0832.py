# Generated by Django 3.1.1 on 2020-09-21 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200917_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='singlechoiceresponse',
            name='user_choice_question_constraint',
        ),
        migrations.RemoveConstraint(
            model_name='textresponse',
            name='user_question_constraint',
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.question'),
        ),
        migrations.AlterField(
            model_name='multiplechoicesresponse',
            name='user',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='singlechoiceresponse',
            name='user',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='textresponse',
            name='user',
            field=models.IntegerField(),
        ),
        migrations.AddConstraint(
            model_name='singlechoiceresponse',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='single_choice_responce_user_question_constraint'),
        ),
        migrations.AddConstraint(
            model_name='textresponse',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='text_response_user_question_constraint'),
        ),
    ]
