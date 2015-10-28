# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crimes',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('index', models.IntegerField(null=True, blank=True)),
                ('incidntnum', models.BigIntegerField(null=True, db_column='IncidntNum', blank=True)),
                ('category', models.TextField(null=True, db_column='Category', blank=True)),
                ('descript', models.TextField(null=True, db_column='Descript', blank=True)),
                ('dayofweek', models.TextField(null=True, db_column='DayOfWeek', blank=True)),
                ('date', models.TextField(null=True, db_column='Date', blank=True)),
                ('time', models.TextField(null=True, db_column='Time', blank=True)),
                ('pddistrict', models.TextField(null=True, db_column='PdDistrict', blank=True)),
                ('resolution', models.TextField(null=True, db_column='Resolution', blank=True)),
                ('address', models.TextField(null=True, db_column='Address', blank=True)),
                ('x', models.FloatField(null=True, db_column='X', blank=True)),
                ('y', models.FloatField(null=True, db_column='Y', blank=True)),
                ('location', models.TextField(null=True, db_column='Location', blank=True)),
                ('pdid', models.BigIntegerField(null=True, db_column='PdId', blank=True)),
                ('datetime', models.DateTimeField(null=True, db_column='DateTime', blank=True)),
                ('city', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'db_table': 'crimes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('orig_lati', models.CharField(max_length=255)),
                ('orig_long', models.CharField(max_length=255)),
                ('dest_lati', models.CharField(max_length=255)),
                ('dest_long', models.CharField(max_length=255)),
            ],
        ),
    ]
