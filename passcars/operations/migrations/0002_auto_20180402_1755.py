# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-02 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='stop_pick',
            field=models.CharField(choices=[('1', '停车'), ('0', '取车')], default='1', max_length=5, verbose_name='停取车'),
        ),
    ]