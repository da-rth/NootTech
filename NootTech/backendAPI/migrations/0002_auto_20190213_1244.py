# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-13 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='upload_key',
            field=models.CharField(default='ahpBX79jQ5aaze6bohojug==', max_length=26),
        ),
    ]