# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_post_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dateOfCreation',
            field=models.DateTimeField(),
        ),
    ]
