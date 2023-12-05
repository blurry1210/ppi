# Generated by Django 4.2.7 on 2023-12-04 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_alter_author_id_alter_category_id_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=tinymce.models.HTMLField(blank=True, default='bio'),
        ),
        migrations.CreateModel(
            name='AuthorAdmin',
            fields=[
                ('fullname', models.CharField(blank=True, max_length=40)),
                ('slug', models.SlugField(blank=True, max_length=400, unique=True)),
                ('bio', tinymce.models.HTMLField(blank=True, default='bio')),
                ('points', models.IntegerField(default=0)),
                ('profile_pic', django_resized.forms.ResizedImageField(blank=True, crop=None, default=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[50, 80], upload_to='authors')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
