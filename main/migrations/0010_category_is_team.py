# Generated by Django 4.2.7 on 2023-12-18 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_author_selected_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_team',
            field=models.BooleanField(default=False),
        ),
    ]
