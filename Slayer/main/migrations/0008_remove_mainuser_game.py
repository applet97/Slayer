# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-15 03:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_mainuser_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainuser',
            name='game',
        ),
    ]
