# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150602_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='login',
            field=models.TextField(unique=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.TextField(max_length=80),
        ),
    ]
