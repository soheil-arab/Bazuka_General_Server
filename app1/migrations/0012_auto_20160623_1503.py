# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20160623_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gem',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='gold',
            field=models.IntegerField(default=0),
        ),
    ]