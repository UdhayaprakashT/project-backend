# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('split_bills_app', '0002_bills'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bills',
            new_name='Bill',
        ),
        migrations.RenameModel(
            old_name='PayGroups',
            new_name='PayGroup',
        ),
    ]
