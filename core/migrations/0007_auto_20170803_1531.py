# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-03 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170803_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_poems',
            name='poet',
        ),
        migrations.AddField(
            model_name='all_poems',
            name='poet',
            field=models.ManyToManyField(blank=True, null=True, to='core.all_authors'),
        ),
    ]