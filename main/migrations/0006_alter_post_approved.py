# Generated by Django 4.2.7 on 2023-12-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_post_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
