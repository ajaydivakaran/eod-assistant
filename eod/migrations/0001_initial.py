# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='EndOfDayItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('done_date', models.DateTimeField(auto_now=True, verbose_name='Task done date')),
                ('contributors', models.ManyToManyField(to='eod.Contributor')),
            ],
        ),
    ]
