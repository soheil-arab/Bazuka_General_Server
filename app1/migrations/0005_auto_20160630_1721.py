# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-30 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_user_basicuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clan',
            name='clanLocation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]