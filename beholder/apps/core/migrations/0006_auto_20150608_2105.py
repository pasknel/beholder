# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150608_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='post',
            new_name='posts',
        ),
    ]
