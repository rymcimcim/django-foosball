# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-12 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_auto_20161012_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='tie_games',
            field=models.IntegerField(default=0),
        ),
    ]
