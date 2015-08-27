# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150616_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='network',
            field=models.CharField(default='Instagram', max_length=255),
            preserve_default=False,
        ),
    ]
