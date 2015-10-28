# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20150928_2251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ends',
            old_name='date',
            new_name='ends_date',
        ),
        migrations.RenameField(
            model_name='ends',
            old_name='time',
            new_name='ends_time',
        ),
        migrations.AlterField(
            model_name='ends',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 23, 3, 21, 392453), blank=True),
        ),
    ]
