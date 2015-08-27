# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_person_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=255)),
                ('post', models.ManyToManyField(to='core.Post')),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='total',
        ),
        migrations.AddField(
            model_name='person',
            name='profile_picture',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
