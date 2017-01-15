# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import eod.models


class Migration(migrations.Migration):

    dependencies = [
        ('eod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='timezone',
            field=models.CharField(default='Asia/Kolkata', max_length=30, validators=[eod.models._validate_known_timezone]),
        ),
    ]