# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-22 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erudit', '0040_article_external_pdf_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='code',
            field=models.CharField(db_index=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='localidentifier',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='localidentifier',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Identifiant Fedora'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='localidentifier',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True, verbose_name='Identifiant Fedora'),
        ),
    ]
