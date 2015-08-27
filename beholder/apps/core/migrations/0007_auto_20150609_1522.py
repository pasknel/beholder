# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150608_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.TextField(max_length=255, unique=True, serialize=False, primary_key=True),
        ),
    ]
