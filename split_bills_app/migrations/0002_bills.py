# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('split_bills_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='split_bills_app.PayGroups')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_paid_by', to=settings.AUTH_USER_MODEL)),
                ('split_between', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
