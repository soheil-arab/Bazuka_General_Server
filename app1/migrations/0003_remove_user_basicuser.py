# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-29 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20160629_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='basicUser',
        ),
    ]