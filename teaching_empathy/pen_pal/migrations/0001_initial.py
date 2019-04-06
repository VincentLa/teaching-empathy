# Generated by Django 2.1.7 on 2019-04-06 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convo_time', models.DateTimeField(auto_now_add=True)),
                ('response', models.TextField()),
                ('seen', models.BooleanField()),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('title', models.TextField()),
                ('authors', models.TextField()),
                ('year_of_publication', models.IntegerField()),
                ('journal', models.TextField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversation_phase', models.IntegerField()),
                ('question_idx', models.IntegerField()),
                ('user1_skip', models.BooleanField()),
                ('user2_skip', models.BooleanField()),
                ('match_time', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField()),
            ],
            options={
                'ordering': ['user1_id'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_match', models.BooleanField()),
                ('new_convo', models.BooleanField()),
                ('seen', models.BooleanField()),
                ('match_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Matches')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_report', models.TextField()),
                ('conversationtext_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.ConversationText')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['conversationtext_id'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer1', models.IntegerField()),
                ('answer2', models.IntegerField()),
                ('answer3', models.IntegerField()),
                ('match_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Matches')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['match_id'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TopicLiterature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('literature_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Literature')),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Topic')),
            ],
            options={
                'ordering': ['topic_id'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('gender', models.TextField(choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('political_status', models.TextField(choices=[('Democrat', 'Democrat'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('Green Party', 'Green Party'), ('Other', 'Other')])),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='UserTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.TextField(choices=[('Very Liberal', 'Very Liberal'), ('Slightly liberal', 'Slightly Liberal'), ('Neutral', 'Neutral'), ('Slightly Conservative', 'Slightly Conservative'), ('Very Conservative', 'Very Conservative')])),
                ('progress', models.IntegerField()),
                ('interest_other_side', models.BooleanField()),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Topic')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['topic_id'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='topic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Topic'),
        ),
        migrations.AddField(
            model_name='matches',
            name='topic1_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='match_topic1', to='pen_pal.Topic'),
        ),
        migrations.AddField(
            model_name='matches',
            name='topic2_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='match_topic2', to='pen_pal.Topic'),
        ),
        migrations.AddField(
            model_name='matches',
            name='topic3_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='match_topic3', to='pen_pal.Topic'),
        ),
        migrations.AddField(
            model_name='matches',
            name='user1_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matches',
            name='user2_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversationtext',
            name='match_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Matches'),
        ),
        migrations.AddField(
            model_name='conversationtext',
            name='question_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Question'),
        ),
        migrations.AddField(
            model_name='conversationtext',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
