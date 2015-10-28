# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20150928_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ends',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 22, 51, 31, 894486), blank=True),
        ),
    ]
