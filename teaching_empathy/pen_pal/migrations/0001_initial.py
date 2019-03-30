# Generated by Django 2.1.7 on 2019-02-25 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.TextField()),
                ('literature_review', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('gender', models.TextField()),
                ('political_status', models.TextField()),
                ('interested_topics', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Topic')),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='topic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pen_pal.Topic'),
        ),
    ]