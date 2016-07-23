# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-20 15:48
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20160711_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewardpack',
            name='slotNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='packEmptySlots',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[None, None, None, None], size=4),
        ),
    ]