# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_app', '0002_auto_20161025_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
