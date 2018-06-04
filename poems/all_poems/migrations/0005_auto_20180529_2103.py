# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-29 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('all_poems', '0004_poems_about_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='作者')),
            ],
            options={
                'verbose_name': '诗人',
                'verbose_name_plural': '诗人',
            },
        ),
        migrations.AlterField(
            model_name='poems',
            name='author',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='all_poems.Author', verbose_name='诗人'),
        ),
    ]