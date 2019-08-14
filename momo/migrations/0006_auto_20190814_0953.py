# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-14 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0005_auto_20190814_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='momorequest',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1235aeac-7d35-4369-b6f7-b4f6ab089b44'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='narration',
            field=models.CharField(default='Testing MoMo API', max_length=50),
        ),
    ]
