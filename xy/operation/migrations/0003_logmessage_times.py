# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-20 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20180420_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='logmessage',
            name='times',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
