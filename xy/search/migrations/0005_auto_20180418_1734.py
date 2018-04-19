# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-18 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20180418_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobbolearticle',
            name='comment_nums',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='评论数'),
        ),
        migrations.AlterField(
            model_name='jobbolearticle',
            name='fav_nums',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='jobbolearticle',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='标签'),
        ),
    ]