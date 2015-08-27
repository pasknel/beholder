# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150717_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.TextField(max_length=255, unique=True, serialize=False, primary_key=True)),
                ('name', models.TextField(max_length=80)),
                ('checkins', models.IntegerField()),
            ],
        ),
    ]
