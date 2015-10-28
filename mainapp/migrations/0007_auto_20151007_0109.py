# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20150929_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ends',
            old_name='city',
            new_name='dest_city',
        ),
        migrations.AddField(
            model_name='ends',
            name='orig_city',
            field=models.CharField(default='San Francisco', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_date',
            field=models.DateField(default=datetime.date(2015, 10, 7), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 1, 8, 47, 601433), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_time',
            field=models.TimeField(default=datetime.time(1, 8, 47, 601518), null=True, blank=True),
        ),
    ]
