# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theJekyllProject', '0010_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='layout',
            field=models.CharField(blank=True, choices=[('post', 'post')], max_length=100, null=True),
        ),
    ]