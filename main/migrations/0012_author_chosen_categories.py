# Generated by Django 4.2.7 on 2023-12-18 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_author_selected_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='chosen_categories',
            field=models.ManyToManyField(blank=True, to='main.category'),
        ),
    ]
