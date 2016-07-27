# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-25 10:30
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20160720_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='backtory_instanceID',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='packEmptySlots',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[1, 1, 1, 1], size=4),
        ),
    ]