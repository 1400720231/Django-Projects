# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-18 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20180418_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobbolearticle',
            name='comment_nums',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AlterField(
            model_name='jobbolearticle',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='收藏数'),
        ),
    ]