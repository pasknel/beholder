# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150609_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='posts',
            new_name='post',
        ),
    ]
