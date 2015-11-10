# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.forms.extras.widgets import SelectDateWidget
import datetime

#from location_field.models.plain import PlainLocationField

#from django.contrib.gis.db import models
#from django.contrib.gis.geos import Point
#from location_field.models.spatial import LocationField

#class Place(models.Model):
#    city = models.CharField(max_length=255)
#    location = LocationField(based_fields=[city], zoom=7, default='Point(1.0 1.0)')
#    objects = models.GeoManager()

class Ends(models.Model):
    orig_city = models.CharField(max_length=255)
    dest_city = models.CharField(max_length=255)
    ends_datetime = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
    ends_date = models.DateField(default=datetime.datetime.now().date(), blank=True, null=True)
    ends_time = models.TimeField(default=datetime.datetime.now().time(), blank=True, null=True )
    orig_lati = models.CharField(max_length=255)#PlainLocationField(based_fields=[city], zoom=7)
    orig_long = models.CharField(max_length=255)#PlainLocationField(based_fields=[city], zoom=7)
    dest_lati = models.CharField(max_length=255)#PlainLocationField(based_fields=[city], zoom=7)
    dest_long = models.CharField(max_length=255)#PlainLocationField(based_fields=[city], zoom=7)



class Crimes(models.Model):
    id = models.IntegerField( primary_key=True)
    #index = models.IntegerField( blank=True, null=True )
    incidntnum = models.BigIntegerField(db_column='IncidntNum', blank=True, null=True)  # Field name made lowercase.
    category = models.TextField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    descript = models.TextField(db_column='Descript', blank=True, null=True)  # Field name made lowercase.
    dayofweek = models.TextField(db_column='DayOfWeek', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TextField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    pddistrict = models.TextField(db_column='PdDistrict', blank=True, null=True)  # Field name made lowercase.
    resolution = models.TextField(db_column='Resolution', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    x = models.FloatField(db_column='X', blank=True, null=True)  # Field name made lowercase.
    y = models.FloatField(db_column='Y', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    pdid = models.BigIntegerField(db_column='PdId', blank=True, null=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=30, blank=True, null=True)
    ns_time = models.TimeField(db_column='ns_time', blank=True, null=True)
    ns_date = models.DateField(db_column='ns_date', blank=True, null=True)
    ns_dayofweek = models.IntegerField(db_column='ns_dayofweek', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crimes'

class PopDensity(models.Model):
    id =  models.IntegerField( primary_key=True)
    index = models.BigIntegerField(blank=True, null=True)
    zip = models.BigIntegerField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    zip_zcta = models.BigIntegerField(db_column='Zip/ZCTA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_2010_population = models.BigIntegerField(db_column='2010 Population', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    land_sq_mi = models.FloatField(db_column='Land-Sq-Mi', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    density = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pop_density'

class Tweets(models.Model):
    tweet_id = models.BigIntegerField(blank=True, null=True)
    datetime = models.TextField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    tweet = models.TextField(blank=True, null=True)
    ns_datetime = models.DateTimeField(blank=True, null=True)
    ns_date = models.DateField(blank=True, null=True)
    ns_time = models.TimeField(blank=True, null=True)
    ns_dayofweek = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    id = models.IntegerField( primary_key=True )

    class Meta:
        managed = False
        db_table = 'tweets'

