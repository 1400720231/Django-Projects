# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-23 13:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_goodscategorybrand_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodscategory',
            options={'verbose_name': '商品类目', 'verbose_name_plural': '商品类目'},
        ),
    ]
