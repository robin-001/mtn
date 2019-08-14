# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-14 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0004_auto_20190814_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='momorequest',
            old_name='momo_referene',
            new_name='momo_reference',
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b6ce67e2-9de1-4128-9d88-34d040cef444'), editable=False, primary_key=True, serialize=False),
        ),
    ]
