# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20150928_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopDensity',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('index', models.BigIntegerField(null=True, blank=True)),
                ('zip', models.BigIntegerField(null=True, blank=True)),
                ('y', models.FloatField(null=True, blank=True)),
                ('x', models.FloatField(null=True, blank=True)),
                ('zip_zcta', models.BigIntegerField(null=True, db_column='Zip/ZCTA', blank=True)),
                ('number_2010_population', models.BigIntegerField(null=True, db_column='2010 Population', blank=True)),
                ('land_sq_mi', models.FloatField(null=True, db_column='Land-Sq-Mi', blank=True)),
                ('density', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'pop_density',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_date',
            field=models.DateField(default=datetime.date(2015, 9, 29), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 17, 13, 39, 71660), blank=True),
        ),
        migrations.AlterField(
            model_name='ends',
            name='ends_time',
            field=models.TimeField(default=datetime.time(17, 13, 39, 71713), null=True, blank=True),
        ),
    ]
