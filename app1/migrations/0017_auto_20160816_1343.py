# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-16 13:43
from __future__ import unicode_literals

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='startTime',
            field=models.IntegerField(default=app1.models.current_time),
        ),
    ]