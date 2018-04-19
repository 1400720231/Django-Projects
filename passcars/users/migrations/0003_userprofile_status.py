# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-03 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180402_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('1', '正在使用'), ('0', '未使用')], default='0', max_length=5),
        ),
    ]