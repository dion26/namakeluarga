# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-23 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='listapp.Person'),
        ),
    ]
