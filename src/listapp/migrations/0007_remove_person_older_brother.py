# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-26 09:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0006_person_older_brother'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='older_brother',
        ),
    ]
