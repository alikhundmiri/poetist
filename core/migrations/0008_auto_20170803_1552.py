# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-03 10:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_auto_20170803_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_poems',
            name='poet',
        ),
        migrations.AddField(
            model_name='all_poems',
            name='poet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='all_riddles',
            name='riddler',
        ),
        migrations.AddField(
            model_name='all_riddles',
            name='riddler',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='all_stories',
            name='author',
        ),
        migrations.AddField(
            model_name='all_stories',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
