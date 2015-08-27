# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='id',
            field=models.AutoField(primary_key=True, auto_created=True, serialize=False, default=1, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='login',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
