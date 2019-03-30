# Generated by Django 2.1.7 on 2019-03-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pen_pal', '0002_auto_20190330_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.TextField(choices=[('Male', 'Male'), ('Female', 'Female')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='political_status',
            field=models.TextField(choices=[('Democrat', 'Democrat'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('Green Party', 'Green Party'), ('Other', 'Other')]),
        ),
    ]