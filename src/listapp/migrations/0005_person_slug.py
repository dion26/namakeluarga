# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-25 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0004_auto_20180223_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]