# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('split_bills_app', '0009_remove_group_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='split_bills_app.CustomUser'),
        ),
    ]
