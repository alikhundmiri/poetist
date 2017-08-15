# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-02 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170701_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_poems',
            name='poet',
            field=models.ManyToManyField(blank=True, null=True, to='core.all_authors'),
        ),
        migrations.AlterField(
            model_name='all_poems',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.taggers'),
        ),
        migrations.AlterField(
            model_name='all_riddles',
            name='riddler',
            field=models.ManyToManyField(blank=True, null=True, to='core.all_authors'),
        ),
        migrations.AlterField(
            model_name='all_riddles',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.taggers'),
        ),
        migrations.AlterField(
            model_name='all_stories',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, to='core.all_authors'),
        ),
        migrations.AlterField(
            model_name='all_stories',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='core.taggers'),
        ),
    ]
