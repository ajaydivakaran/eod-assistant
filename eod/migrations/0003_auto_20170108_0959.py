# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eod', '0002_auto_20170108_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='display_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
