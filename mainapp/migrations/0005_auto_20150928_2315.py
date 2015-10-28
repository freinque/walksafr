# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20150928_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ends',
            name='datetime',
        ),
        migrations.AddField(
            model_name='ends',
            name='ends_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 23, 15, 47, 693174), blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_date',
            field=models.DateField(default=datetime.date(2015, 9, 28), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_time',
            field=models.TimeField(default=datetime.time(23, 15, 47, 693285), null=True, blank=True),
        ),
    ]
