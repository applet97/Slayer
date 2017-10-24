# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-15 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_mainuser_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_players', to='main.Game'),
        ),
    ]
