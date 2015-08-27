# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150602_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
