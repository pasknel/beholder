# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150610_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='text',
            field=models.TextField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='connection',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
