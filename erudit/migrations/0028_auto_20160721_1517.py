# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erudit', '0027_auto_20160721_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='open_access',
        ),
        migrations.AlterField(
            model_name='journal',
            name='open_access',
            field=models.BooleanField(default=False, help_text='Cette revue est en accès libre?', verbose_name='Libre accès'),
        ),
    ]
