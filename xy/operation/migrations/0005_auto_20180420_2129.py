# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-20 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_auto_20180420_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmessage',
            name='times',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='查询次数'),
        ),
    ]