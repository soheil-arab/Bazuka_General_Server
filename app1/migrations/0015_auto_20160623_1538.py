# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_auto_20160623_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clan',
            name='clanTag',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True, unique=True),
        ),
    ]