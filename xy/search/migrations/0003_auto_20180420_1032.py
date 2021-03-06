# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-20 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20180418_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(default='', max_length=100, verbose_name='历史搜索')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
