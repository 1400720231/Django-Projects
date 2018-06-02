# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-31 12:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('all_poems', '0010_auto_20180529_2345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Praise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_poems.Poems', verbose_name='点赞诗词')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞用户')),
            ],
            options={
                'verbose_name': '点赞信息',
                'verbose_name_plural': '点赞信息',
            },
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-date_time'], 'verbose_name': '评论信息', 'verbose_name_plural': '评论信息'},
        ),
    ]
