# Generated by Django 4.2.7 on 2023-12-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210618_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
