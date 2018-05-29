# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-29 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_poems', '0009_auto_20180529_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poems',
            name='poem_type',
        ),
        migrations.AddField(
            model_name='poems',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='标签'),
        ),
    ]
